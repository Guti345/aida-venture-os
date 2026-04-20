"""
Servicio de generación de reportes para LPs — AIDA Venture OS.
Agrega datos de todos los dominios para producir vistas ejecutivas.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.models.fund import Fund, FundMetric, Investment
from app.models.startup import MetricSnapshot, Startup, StartupStatus
from app.models.studio import StudioCompany
from app.models.dealflow import DealOpportunity, DealStatus
from app.schemas.reporting import LPReportSummary, PortfolioSnapshotItem


def _latest_metric(db: Session, startup_id, metric_name: str) -> float | None:
    snap = (
        db.query(MetricSnapshot)
        .filter(
            MetricSnapshot.startup_id == startup_id,
            MetricSnapshot.metric_name == metric_name,
        )
        .order_by(desc(MetricSnapshot.period_date))
        .first()
    )
    return float(snap.value) if snap else None


def generate_lp_report(db: Session) -> LPReportSummary:
    # Fondo activo
    fund: Fund | None = db.query(Fund).first()
    fund_name = fund.name if fund else "AIDA Ventures Fund I"

    # Métricas más recientes del fondo
    latest_metric_row: FundMetric | None = None
    if fund:
        latest_metric_row = (
            db.query(FundMetric)
            .filter(FundMetric.fund_id == fund.id)
            .order_by(desc(FundMetric.calculation_date))
            .first()
        )

    total_invested = float(latest_metric_row.total_invested_usd) if latest_metric_row else 0.0
    fund_moic = float(latest_metric_row.moic) if latest_metric_row else None
    fund_irr = float(latest_metric_row.irr) if (latest_metric_row and latest_metric_row.irr) else None

    # Startups activas
    active_startups: list[Startup] = (
        db.query(Startup)
        .filter(Startup.status == StartupStatus.active)
        .all()
    )
    portfolio_count = len(active_startups)
    active_count = portfolio_count

    # Empresas del studio
    studio_count = db.query(StudioCompany).count()

    # Graduation rate del studio
    graduated = db.query(StudioCompany).filter(
        StudioCompany.first_external_seed_date.isnot(None)
    ).count()
    graduation_rate = round(graduated / studio_count * 100, 2) if studio_count > 0 else 0.0

    # Top performers: startups con NRR > 110
    top_performers: list[str] = []
    for startup in active_startups:
        nrr = _latest_metric(db, startup.id, "NRR_pct")
        if nrr is not None and nrr > 110:
            top_performers.append(startup.name)

    # Pipeline de deals
    all_deals = db.query(DealOpportunity).all()
    pipeline_statuses = {DealStatus.identified, DealStatus.screening, DealStatus.dd, DealStatus.ic}
    deals_in_pipeline = sum(1 for d in all_deals if d.status in pipeline_statuses)

    this_year = date.today().year
    deals_invested_this_year = sum(
        1 for d in all_deals
        if d.status == DealStatus.invested and d.identified_at.year == this_year
    )

    # Narrative summary generado con datos reales
    top_str = (", ".join(top_performers) if top_performers else "en evaluación")
    moic_str = f"{fund_moic:.2f}x MOIC" if fund_moic else "MOIC pendiente de cálculo"
    narrative = (
        f"AIDA Ventures Fund I opera con {portfolio_count} empresas activas en portafolio "
        f"y {studio_count} en construcción dentro del venture studio, con una tasa de graduación "
        f"a Seed externo del {graduation_rate}%. "
        f"El fondo muestra {moic_str} sobre ${total_invested:,.0f} USD desplegados, "
        f"con {deals_in_pipeline} deals activos en pipeline y top performers en NRR: {top_str}. "
        f"El studio genera alpha medible en graduation rate y supervivencia vs. el mercado LATAM."
    )

    return LPReportSummary(
        fund_name=fund_name,
        report_date=date.today(),
        total_invested_usd=total_invested,
        portfolio_companies=portfolio_count,
        active_companies=active_count,
        studio_companies=studio_count,
        top_performers=top_performers,
        fund_moic_current=fund_moic,
        fund_irr_current=fund_irr,
        deals_in_pipeline=deals_in_pipeline,
        deals_invested_this_year=deals_invested_this_year,
        studio_graduation_rate_pct=graduation_rate,
        narrative_summary=narrative,
    )


def get_portfolio_snapshot(db: Session) -> list[PortfolioSnapshotItem]:
    startups: list[Startup] = (
        db.query(Startup)
        .filter(Startup.status == StartupStatus.active)
        .order_by(Startup.name)
        .all()
    )

    items: list[PortfolioSnapshotItem] = []
    for s in startups:
        arr = _latest_metric(db, s.id, "ARR")
        mrr = _latest_metric(db, s.id, "MRR")
        nrr = _latest_metric(db, s.id, "NRR_pct")
        burn = _latest_metric(db, s.id, "burn_multiple")
        runway = _latest_metric(db, s.id, "runway_months")
        yoy = _latest_metric(db, s.id, "YoY_growth_pct")

        items.append(PortfolioSnapshotItem(
            startup_name=s.name,
            sector=s.sector,
            stage=s.stage.value,
            country=s.country,
            arr_usd=arr,
            mrr_usd=mrr,
            yoy_growth_pct=yoy,
            burn_multiple=burn,
            runway_months=runway,
            nrr_pct=nrr,
            status=s.status.value,
        ))

    return items
