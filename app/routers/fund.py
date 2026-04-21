import uuid
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.fund import Fund, FundMetric, FundScenario, Investment
from app.schemas.fund import (
    FundMetricsRead, FundRead, FundScenarioRead, InvestmentRead,
    ScenarioInput, ScenarioResult,
)
from app.models.shared import User
from app.services.auth import require_analyst
from app.services.simulator import run_monte_carlo

router = APIRouter(prefix="/fund", tags=["fund"])


class ScenarioLabel(str, Enum):
    conservador = "conservador"
    base = "base"
    optimista = "optimista"


_SCENARIO_PRESETS: dict[str, dict] = {
    "conservador": {"pct_winners": 0.10, "avg_winner_multiple": 8.0},
    "base":        {"pct_winners": 0.20, "avg_winner_multiple": 15.0},
    "optimista":   {"pct_winners": 0.35, "avg_winner_multiple": 20.0},
}


def _active_fund(db: Session) -> Fund:
    fund = db.query(Fund).first()
    if fund is None:
        raise HTTPException(status_code=404, detail="No hay ningún fondo registrado en la base de datos")
    return fund


@router.get("", response_model=FundRead)
def get_fund(db: Session = Depends(get_db)):
    return _active_fund(db)


@router.get("/investments", response_model=list[InvestmentRead])
def list_investments(db: Session = Depends(get_db)):
    fund = _active_fund(db)
    investments = (
        db.query(Investment)
        .options(joinedload(Investment.startup))
        .filter(Investment.fund_id == fund.id)
        .order_by(Investment.date.desc())
        .all()
    )
    return [InvestmentRead.from_orm_with_name(inv) for inv in investments]


@router.get("/metrics", response_model=FundMetricsRead)
def get_fund_metrics(db: Session = Depends(get_db)):
    fund = _active_fund(db)
    metric = (
        db.query(FundMetric)
        .filter(FundMetric.fund_id == fund.id)
        .order_by(desc(FundMetric.calculation_date))
        .first()
    )
    if metric is None:
        raise HTTPException(
            status_code=404,
            detail="No hay métricas calculadas para este fondo. Ejecuta POST /fund/simulate primero.",
        )
    return metric


@router.get("/scenarios", response_model=list[FundScenarioRead])
def list_scenarios(db: Session = Depends(get_db)):
    fund = _active_fund(db)
    return (
        db.query(FundScenario)
        .filter(FundScenario.fund_id == fund.id)
        .order_by(desc(FundScenario.run_date))
        .all()
    )


@router.post("/simulate", response_model=ScenarioResult)
def simulate(inp: ScenarioInput, db: Session = Depends(get_db), _user: User = Depends(require_analyst)):
    result = run_monte_carlo(db, inp)
    db.commit()
    return result


@router.get("/simulate/quick", response_model=ScenarioResult)
def simulate_quick(
    scenario_label: ScenarioLabel = Query(default=ScenarioLabel.base, description="Perfil de escenario: conservador, base u optimista"),
    pct_winners: Optional[float] = Query(default=None, description="Porcentaje de deals ganadores (0.0–1.0). Sobreescribe scenario_label si se provee."),
    avg_winner_multiple: Optional[float] = Query(default=None, description="Múltiplo promedio de deals ganadores. Sobreescribe scenario_label si se provee."),
    db: Session = Depends(get_db),
):
    """Ejecuta Monte Carlo con presets por escenario. Usa scenario_label para seleccionar
    conservador (10% winners, 8x), base (20%, 15x) u optimista (35%, 20x).
    Los parámetros pct_winners y avg_winner_multiple sobreescriben el preset si se proveen.
    """
    fund = _active_fund(db)
    preset = _SCENARIO_PRESETS[scenario_label.value]

    resolved_pct = pct_winners if pct_winners is not None else preset["pct_winners"]
    resolved_multiple = avg_winner_multiple if avg_winner_multiple is not None else preset["avg_winner_multiple"]

    inp = ScenarioInput(
        fund_id=fund.id,
        pct_winners=resolved_pct,
        avg_winner_multiple=resolved_multiple,
    )
    result = run_monte_carlo(db, inp)
    db.commit()
    return result
