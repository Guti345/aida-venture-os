"""
Servicio de Studio Performance — cálculo de alpha vs mercado,
resúmenes del portfolio del studio y líneas de tiempo por empresa.
"""

from __future__ import annotations

import uuid
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.studio import AlphaMetric, BuildCost, StudioCompany, StudioMilestone
from app.schemas.studio import AlphaMetricRead, StudioSummary, TimelineEvent


def get_studio_summary(db: Session) -> StudioSummary:
    companies: list[StudioCompany] = (
        db.query(StudioCompany)
        .options(joinedload(StudioCompany.alpha_metrics))
        .all()
    )

    total = len(companies)

    # Conteo por fase
    by_phase: dict[str, int] = {}
    for sc in companies:
        phase = sc.current_studio_phase.value
        by_phase[phase] = by_phase.get(phase, 0) + 1

    # Costos acumulados
    total_cost = sum(float(sc.build_cost_usd) for sc in companies)
    avg_cost = total_cost / total if total > 0 else 0.0

    # Graduation rate = empresas que llegaron a seed externo / total
    graduated = sum(1 for sc in companies if sc.first_external_seed_date is not None)
    graduation_rate = round(graduated / total * 100, 2) if total > 0 else 0.0

    # Promedio meses idea → mvp (solo empresas con ambas fechas)
    deltas_months: list[float] = []
    for sc in companies:
        if sc.idea_date and sc.mvp_date:
            delta_days = (sc.mvp_date - sc.idea_date).days
            deltas_months.append(delta_days / 30.44)
    avg_months = round(sum(deltas_months) / len(deltas_months), 1) if deltas_months else None

    # Alpha metrics is_alpha=True (de cualquier empresa del studio)
    alpha_rows: list[AlphaMetric] = (
        db.query(AlphaMetric)
        .filter(AlphaMetric.is_alpha.is_(True))
        .all()
    )

    return StudioSummary(
        total_companies=total,
        companies_by_phase=by_phase,
        total_build_cost_usd=round(total_cost, 2),
        avg_build_cost_usd=round(avg_cost, 2),
        graduation_rate_pct=graduation_rate,
        avg_months_idea_to_mvp=avg_months,
        alpha_vs_market=[AlphaMetricRead.model_validate(a) for a in alpha_rows],
    )


def get_company_timeline(db: Session, studio_company_id: uuid.UUID) -> list[TimelineEvent]:
    sc: StudioCompany | None = db.get(StudioCompany, studio_company_id)
    if sc is None:
        raise HTTPException(status_code=404, detail="StudioCompany no encontrada")

    milestones: list[StudioMilestone] = (
        db.query(StudioMilestone)
        .filter(
            StudioMilestone.studio_company_id == studio_company_id,
            StudioMilestone.achieved.is_(True),
            StudioMilestone.actual_date.isnot(None),
        )
        .all()
    )

    events: list[TimelineEvent] = []

    # Fechas de hitos del propio StudioCompany
    _PHASE_LABELS = {
        "idea_date":                  ("idea",            "Empresa creada — fase Idea iniciada"),
        "validation_date":            ("validation",      "Hipótesis de negocio validada con primeros clientes"),
        "mvp_date":                   ("mvp",             "MVP lanzado al mercado"),
        "pmf_date":                   ("pmf",             "Product-Market Fit alcanzado"),
        "first_external_seed_date":   ("seed_externo",    "Primera ronda Seed externa cerrada — graduación del studio"),
    }
    for attr, (etype, desc) in _PHASE_LABELS.items():
        d: date | None = getattr(sc, attr)
        if d is not None:
            events.append(TimelineEvent(date=d, event_type=etype, description=desc))

    # Hitos achieved de StudioMilestone
    for m in milestones:
        events.append(
            TimelineEvent(
                date=m.actual_date,
                event_type=m.milestone_type.value,
                description=f"Hito '{m.milestone_type.value}' alcanzado"
                + (f" — {m.notes}" if m.notes else ""),
            )
        )

    # Ordenar cronológicamente y deduplicar por fecha+tipo
    seen: set[tuple] = set()
    unique: list[TimelineEvent] = []
    for ev in sorted(events, key=lambda e: e.date):
        key = (ev.date, ev.event_type)
        if key not in seen:
            seen.add(key)
            unique.append(ev)

    return unique


def calculate_alpha_score(db: Session, studio_company_id: uuid.UUID) -> dict:
    sc: StudioCompany | None = db.get(StudioCompany, studio_company_id)
    if sc is None:
        raise HTTPException(status_code=404, detail="StudioCompany no encontrada")

    metrics: list[AlphaMetric] = (
        db.query(AlphaMetric)
        .filter(AlphaMetric.studio_company_id == studio_company_id)
        .all()
    )

    if not metrics:
        return {
            "studio_company_id": studio_company_id,
            "alpha_score": 0,
            "metrics_evaluated": 0,
            "metrics_above_benchmark": 0,
            "detail": [],
        }

    with_benchmark = [m for m in metrics if m.market_benchmark is not None]
    above = [m for m in with_benchmark if m.is_alpha is True]

    score = round(len(above) / len(with_benchmark) * 100, 1) if with_benchmark else 0.0

    detail = [
        {
            "metric_name": m.metric_name,
            "studio_value": float(m.studio_value),
            "market_benchmark": float(m.market_benchmark) if m.market_benchmark else None,
            "delta_pct": float(m.delta_pct) if m.delta_pct else None,
            "is_alpha": m.is_alpha,
        }
        for m in with_benchmark
    ]

    return {
        "studio_company_id": studio_company_id,
        "alpha_score": score,
        "metrics_evaluated": len(with_benchmark),
        "metrics_above_benchmark": len(above),
        "detail": detail,
    }
