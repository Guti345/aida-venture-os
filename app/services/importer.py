from datetime import date
from typing import Any

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.startup import MetricSnapshot, PeriodType, Startup
from app.schemas.startup import MetricIngestionForm, MetricIngestionResult

_FIELD_TO_METRIC: list[tuple[str, str, str | None, str | None]] = [
    # (form_field, metric_name, unit, currency)
    ("arr_usd",              "ARR",              "USD",     "USD"),
    ("mrr_usd",              "MRR",              "USD",     "USD"),
    ("mom_growth_pct",       "MoM_growth_pct",   "pct",     None),
    ("burn_rate_monthly_usd","burn_rate_monthly", "USD",     "USD"),
    ("runway_months",        "runway_months",     "months",  None),
    ("gross_margin_pct",     "gross_margin_pct",  "pct",     None),
    ("active_customers",     "active_customers",  "count",   None),
    ("cac_usd",              "CAC",               "USD",     "USD"),
    ("ltv_usd",              "LTV",               "USD",     "USD"),
    ("nrr_pct",              "NRR_pct",           "pct",     None),
    ("headcount",            "headcount",         "count",   None),
]


def ingest_metrics(db: Session, form: MetricIngestionForm) -> MetricIngestionResult:
    startup = (
        db.query(Startup)
        .filter(func.lower(Startup.name) == form.startup_name.lower())
        .first()
    )
    if startup is None:
        raise HTTPException(status_code=404, detail=f"Startup '{form.startup_name}' no encontrada")

    saved = 0
    skipped = 0
    warnings: list[str] = []

    form_data: dict[str, Any] = form.model_dump()

    # Compute burn_multiple for warning check (ARR / burn_rate)
    arr = form_data.get("arr_usd")
    burn = form_data.get("burn_rate_monthly_usd")
    if arr and burn and burn > 0:
        burn_multiple = (burn * 12) / arr
        if burn_multiple > 5:
            warnings.append(f"burn_multiple={burn_multiple:.1f} — inusualmente alto (>5)")

    if form_data.get("runway_months") is not None and form_data["runway_months"] < 6:
        warnings.append(f"runway_months={form_data['runway_months']} — runway crítico (<6 meses)")

    if form_data.get("nrr_pct") is not None and form_data["nrr_pct"] < 80:
        warnings.append(f"nrr_pct={form_data['nrr_pct']} — retención preocupante (<80%)")

    for field, metric_name, unit, currency in _FIELD_TO_METRIC:
        value = form_data.get(field)
        if value is None:
            skipped += 1
            continue

        existing = (
            db.query(MetricSnapshot)
            .filter(
                MetricSnapshot.startup_id == startup.id,
                MetricSnapshot.metric_name == metric_name,
                MetricSnapshot.period_date == form.period_date,
            )
            .first()
        )
        if existing:
            existing.value = float(value)
            existing.notes = form.notes
        else:
            snapshot = MetricSnapshot(
                startup_id=startup.id,
                metric_name=metric_name,
                value=float(value),
                unit=unit,
                currency=currency,
                period_date=form.period_date,
                period_type=PeriodType.monthly,
                source="ingesta_manual",
                notes=form.notes,
            )
            db.add(snapshot)
        saved += 1

    db.commit()

    return MetricIngestionResult(
        startup_name=startup.name,
        period_date=form.period_date,
        metrics_saved=saved,
        skipped=skipped,
        warnings=warnings,
    )
