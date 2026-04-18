"""
Motor Monte Carlo para el Fund Simulator de AIDA Venture OS.

Cada iteración asigna aleatoriamente a cada inversión un outcome (winner/loser)
y calcula el MOIC del fondo. Los percentiles p25/p50/p75 se calculan con numpy
sobre N iteraciones. El IRR se aproxima como MOIC^(1/years) - 1.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone

import numpy as np
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.models.fund import Fund, FundMetric, FundScenario, Investment, ScenarioType
from app.schemas.fund import ScenarioInput, ScenarioResult


def _classify_scenario(pct_winners: float, avg_winner_multiple: float) -> ScenarioType:
    """Clasifica el escenario según los parámetros de entrada."""
    if pct_winners >= 0.30 and avg_winner_multiple >= 20.0:
        return ScenarioType.high
    if pct_winners <= 0.12 or avg_winner_multiple <= 8.0:
        return ScenarioType.downside
    return ScenarioType.base


def _run_iterations(
    amounts: np.ndarray,
    n_iterations: int,
    pct_winners: float,
    avg_winner_multiple: float,
    avg_loss_rate: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Corre N iteraciones Monte Carlo vectorizadas.
    Retorna un array 1-D de MOICs (un valor por iteración).
    """
    n_deals = len(amounts)
    total_invested = amounts.sum()

    # Shape: (n_iterations, n_deals)
    is_winner = rng.random((n_iterations, n_deals)) < pct_winners

    # Winners: múltiplo uniforme entre 1x y avg_winner_multiple * 2
    winner_multiples = rng.uniform(1.0, avg_winner_multiple * 2.0, (n_iterations, n_deals))

    # Losers: retorno entre 0 y amount * (1 - avg_loss_rate)
    loss_multiples = rng.uniform(0.0, 1.0 - avg_loss_rate, (n_iterations, n_deals))

    multiples = np.where(is_winner, winner_multiples, loss_multiples)
    returns = (multiples * amounts).sum(axis=1)   # suma por iteración

    return returns / total_invested  # MOIC por iteración


def run_monte_carlo(db: Session, inp: ScenarioInput) -> ScenarioResult:
    # 1. Cargar fondo e inversiones
    fund = db.get(Fund, inp.fund_id)
    if fund is None:
        raise HTTPException(status_code=404, detail=f"Fondo '{inp.fund_id}' no encontrado")

    investments: list[Investment] = (
        db.query(Investment)
        .options(joinedload(Investment.startup))
        .filter(Investment.fund_id == inp.fund_id)
        .all()
    )
    if not investments:
        raise HTTPException(
            status_code=422,
            detail=f"El fondo '{inp.fund_id}' no tiene inversiones registradas",
        )

    amounts = np.array([float(inv.amount_usd) for inv in investments])
    total_invested = float(amounts.sum())

    # 2. Monte Carlo
    rng = np.random.default_rng()
    moics = _run_iterations(
        amounts,
        inp.n_iterations,
        inp.pct_winners,
        inp.avg_winner_multiple,
        inp.avg_loss_rate,
        rng,
    )

    # 3. Percentiles MOIC
    moic_p25 = float(np.percentile(moics, 25))
    moic_p50 = float(np.percentile(moics, 50))
    moic_p75 = float(np.percentile(moics, 75))

    # 4. IRR aproximado por percentil: IRR = MOIC^(1/years) - 1
    def _irr(moic: float) -> float:
        if moic <= 0:
            return -1.0
        return round(moic ** (1.0 / inp.fund_life_years) - 1.0, 6)

    irr_p25 = _irr(moic_p25)
    irr_p50 = _irr(moic_p50)
    irr_p75 = _irr(moic_p75)

    # 5. DPI y TVPI proyectados usando el escenario base (mediana)
    # DPI = retornos distribuidos / capital invertido (aquí proyectado como el 80% del MOIC)
    # TVPI = DPI + RVPI (asumimos RVPI residual = 20% del MOIC)
    dpi_projected = round(moic_p50 * 0.80, 4)
    tvpi_projected = round(moic_p50, 4)

    # 6. Clasificar escenario
    scenario_type = _classify_scenario(inp.pct_winners, inp.avg_winner_multiple)

    # 7. Armar dict de assumptions para persistir
    assumptions = {
        "n_iterations": inp.n_iterations,
        "pct_winners": inp.pct_winners,
        "avg_winner_multiple": inp.avg_winner_multiple,
        "avg_loss_rate": inp.avg_loss_rate,
        "fund_life_years": inp.fund_life_years,
        "mgmt_fee_pct": inp.mgmt_fee_pct,
        "carry_pct": inp.carry_pct,
        "n_investments": len(investments),
        "total_invested_usd": total_invested,
    }

    # 8. Persistir FundScenario
    scenario = FundScenario(
        fund_id=inp.fund_id,
        scenario_type=scenario_type,
        moic_p25=round(moic_p25, 4),
        moic_p50=round(moic_p50, 4),
        moic_p75=round(moic_p75, 4),
        irr_p25=irr_p25,
        irr_p50=irr_p50,
        irr_p75=irr_p75,
        dpi_projected=dpi_projected,
        tvpi_projected=tvpi_projected,
        run_date=datetime.now(timezone.utc),
        assumptions_json=assumptions,
    )
    db.add(scenario)

    # 9. Calcular y persistir FundMetrics actuales
    # FMV actual: pre_money_val de cada inversión * equity_pct como proxy simple
    fmv_estimates = []
    for inv in investments:
        if inv.pre_money_val:
            fmv = float(inv.pre_money_val) * float(inv.equity_pct) / 100.0
        else:
            fmv = float(inv.amount_usd)  # fallback: at-cost
        fmv_estimates.append(fmv)

    total_fmv = sum(fmv_estimates)
    total_realized = 0.0  # sin exits todavía en datos simulados

    current_moic = (total_fmv + total_realized) / total_invested if total_invested > 0 else 1.0
    tvpi_current = current_moic
    dpi_current = total_realized / total_invested if total_invested > 0 else 0.0
    rvpi_current = total_fmv / total_invested if total_invested > 0 else 0.0

    metrics = FundMetric(
        fund_id=inp.fund_id,
        calculation_date=date.today(),
        moic=round(current_moic, 4),
        tvpi=round(tvpi_current, 4),
        dpi=round(dpi_current, 4),
        rvpi=round(rvpi_current, 4),
        irr=None,
        total_invested_usd=total_invested,
        total_fmv_usd=total_fmv,
        total_realized_usd=total_realized,
    )
    db.add(metrics)
    db.flush()

    return ScenarioResult(
        scenario_type=scenario_type,
        moic_p25=round(moic_p25, 4),
        moic_p50=round(moic_p50, 4),
        moic_p75=round(moic_p75, 4),
        irr_p25=irr_p25,
        irr_p50=irr_p50,
        irr_p75=irr_p75,
        dpi_projected=dpi_projected,
        tvpi_projected=tvpi_projected,
        total_invested_usd=total_invested,
        n_iterations=inp.n_iterations,
        assumptions=assumptions,
    )
