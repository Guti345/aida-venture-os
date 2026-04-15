"""
AIDA Venture OS — Unified Seed Loader
Inserta todos los datos simulados en la base de datos respetando el orden de FKs.
Idempotente: re-ejecutable sin errores si los datos ya existen.

Uso: python data/load_seed.py
Requiere: tablas creadas con `alembic upgrade head`
"""

import sys
import uuid
from datetime import date
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from app.database import SessionLocal
import app.models  # noqa: F401 — registers all mappers on Base.metadata

from app.models.fund import Fund, LP, Investment, FundStatus, InvestmentType
from app.models.startup import (
    Startup, Founder, StartupFounder, FundingRound, MetricSnapshot,
    StartupStage, StartupStatus, RoundType, RoundStatus, PeriodType,
)
from app.models.studio import (
    StudioCompany, BuildCost, StudioMilestone, AlphaMetric,
    StudioSupportLevel, StudioPhase, BuildCostType, MilestoneType,
)

from data.seed_data import (
    FUND, STARTUPS, FOUNDERS, FUNDING_ROUNDS, INVESTMENTS,
    METRIC_SNAPSHOTS, STUDIO_COMPANIES as PORTFOLIO_STUDIO_COMPANIES,
)
from data.studio_seed_data import (
    STUDIO_STARTUPS, STUDIO_FOUNDERS, STUDIO_COMPANIES,
    STUDIO_MILESTONES, STUDIO_BUILD_COSTS, STUDIO_METRICS,
    STUDIO_ALPHA_BENCHMARKS,
)

# ── Deterministic UUID generation ────────────────────────────────────────────
# Fixed namespace ensures the same string always produces the same UUID,
# making the script idempotent across runs.
_NS = uuid.UUID("a1da0000-0000-4000-8000-000000000001")


def sid(s: str) -> uuid.UUID:
    """Convert a seed string ID (e.g. 'startup-001') to a stable UUID."""
    return uuid.uuid5(_NS, s)


# ── Enum value mappers ────────────────────────────────────────────────────────

_STAGE_MAP = {
    "pre-seed": StartupStage.pre_seed,
    "seed":     StartupStage.seed,
    "series a": StartupStage.series_a,
    "series b": StartupStage.series_b,
    "bridge":   StartupStage.bridge,
}

_STATUS_MAP = {
    "active":    StartupStatus.active,
    "exited":    StartupStatus.exited,
    "dead":      StartupStatus.dead,
    "watchlist": StartupStatus.watchlist,
}

_ROUND_TYPE_MAP = {
    "pre_seed": RoundType.pre_seed,
    "seed":     RoundType.seed,
    "series_a": RoundType.series_a,
    "series_b": RoundType.series_b,
    "bridge":   RoundType.bridge,
}

_ROUND_STATUS_MAP = {
    "closed":    RoundStatus.closed,
    "announced": RoundStatus.announced,
    "rumored":   RoundStatus.rumored,
}

_INVESTMENT_TYPE_MAP = {
    "lead":      InvestmentType.lead,
    "co_invest": InvestmentType.co_invest,
    "follow_on": InvestmentType.follow_on,
}

_SUPPORT_MAP = {
    "full":        StudioSupportLevel.full,
    "partial":     StudioSupportLevel.partial,
    "accelerator": StudioSupportLevel.accelerator,
}

_PHASE_MAP = {
    "idea":          StudioPhase.idea,
    "validation":    StudioPhase.validation,
    "mvp":           StudioPhase.mvp,
    "first_revenue": StudioPhase.first_revenue,
    "pmf":           StudioPhase.pmf,
    "seed":          StudioPhase.seed,
    "series_a_prep": StudioPhase.series_a_prep,
}

_COST_TYPE_MAP = {
    "personnel": BuildCostType.personnel,
    "tech":      BuildCostType.tech,
    "ops":       BuildCostType.ops,
    "legal":     BuildCostType.legal,
    "marketing": BuildCostType.marketing,
    "capex":     BuildCostType.capex,
}

_MILESTONE_MAP = {
    "idea":          MilestoneType.idea,
    "validation":    MilestoneType.validation,
    "mvp":           MilestoneType.mvp,
    "first_revenue": MilestoneType.first_revenue,
    "pmf":           MilestoneType.pmf,
    "seed":          MilestoneType.seed,
    "series_a":      MilestoneType.series_a,
}


def _d(s: str | None) -> date | None:
    """Parse ISO date string to date, or return None."""
    return date.fromisoformat(s) if s else None


# ── Insert helpers ────────────────────────────────────────────────────────────

def _get_or_skip(db: Session, model, pk: uuid.UUID):
    """Return existing record or None (signals: skip insert)."""
    return db.get(model, pk)


def insert_fund(db: Session) -> tuple[Fund, int]:
    pk = sid(FUND["id"])
    if _get_or_skip(db, Fund, pk):
        return db.get(Fund, pk), 0
    fund = Fund(
        id=pk,
        name=FUND["name"],
        vintage_year=FUND["vintage_year"],
        target_size_usd=FUND["target_size_usd"],
        deployed_usd=FUND["deployed_usd"],
        currency=FUND["currency"],
        geography_focus=FUND["geography_focus"],
        stage_focus=FUND["stage_focus"],
        status=FundStatus[FUND["status"]],
    )
    db.add(fund)
    db.flush()
    return fund, 1


def insert_startups(db: Session) -> int:
    count = 0
    all_startups = [
        {**s, "is_simulated": True} for s in STARTUPS
    ] + list(STUDIO_STARTUPS)

    for s in all_startups:
        pk = sid(s["id"])
        if _get_or_skip(db, Startup, pk):
            continue
        startup = Startup(
            id=pk,
            name=s["name"],
            sector=s["sector"],
            subsector=s.get("subsector"),
            stage=_STAGE_MAP[s["stage"].lower()],
            geography=s.get("geography"),
            country=s.get("country"),
            city=s.get("city"),
            founded_at=_d(s.get("founded_at")),
            studio_built=s.get("studio_built", False),
            website=s.get("website"),
            description=s.get("description"),
            status=_STATUS_MAP[s.get("status", "active")],
            is_simulated=s.get("is_simulated", True),
        )
        db.add(startup)
        count += 1
    db.flush()
    return count


def insert_founders(db: Session) -> int:
    count = 0
    all_founders = list(FOUNDERS) + list(STUDIO_FOUNDERS)

    seen_emails: set[str] = set()
    for f in all_founders:
        pk = sid(f["id"])
        email = f.get("email")
        if _get_or_skip(db, Founder, pk):
            if email:
                seen_emails.add(email)
            continue
        founder = Founder(
            id=pk,
            name=f["name"],
            email=email,
            background=f.get("background"),
        )
        db.add(founder)
        if email:
            seen_emails.add(email)
        count += 1
    db.flush()
    return count


def insert_startup_founders(db: Session) -> int:
    count = 0
    all_founders = list(FOUNDERS) + list(STUDIO_FOUNDERS)

    for f in all_founders:
        founder_pk = sid(f["id"])
        startup_pk = sid(f["startup_id"])
        existing = db.get(StartupFounder, (startup_pk, founder_pk))
        if existing:
            continue
        sf = StartupFounder(
            startup_id=startup_pk,
            founder_id=founder_pk,
            role=f.get("role"),
            equity_pct=f.get("equity_pct"),
            active=True,
        )
        db.add(sf)
        count += 1
    db.flush()
    return count


def insert_funding_rounds(db: Session) -> int:
    count = 0
    for r in FUNDING_ROUNDS:
        pk = sid(r["id"])
        if _get_or_skip(db, FundingRound, pk):
            continue
        rnd = FundingRound(
            id=pk,
            startup_id=sid(r["startup_id"]),
            round_type=_ROUND_TYPE_MAP[r["round_type"]],
            amount_usd=r.get("amount_usd"),
            pre_money_val=r.get("pre_money_val"),
            post_money_val=r.get("post_money_val"),
            lead_investor=r.get("lead_investor"),
            date=_d(r.get("date")),
            status=_ROUND_STATUS_MAP[r.get("status", "closed")],
        )
        db.add(rnd)
        count += 1
    db.flush()
    return count


def insert_investments(db: Session) -> int:
    count = 0
    for i in INVESTMENTS:
        # Investments have no string ID in seed data — derive from startup+round
        pk = sid(f"inv-{i['startup_id']}-{i['round_id']}")
        if _get_or_skip(db, Investment, pk):
            continue
        inv = Investment(
            id=pk,
            startup_id=sid(i["startup_id"]),
            fund_id=sid(i["fund_id"]),
            round_id=sid(i["round_id"]) if i.get("round_id") else None,
            amount_usd=i["amount_usd"],
            pre_money_val=i.get("pre_money_val"),
            equity_pct=i["equity_pct"],
            date=_d(i["date"]),
            investment_type=_INVESTMENT_TYPE_MAP[i["investment_type"]],
            follow_on_reserve_usd=i.get("follow_on_reserve_usd", 0),
        )
        db.add(inv)
        count += 1
    db.flush()
    return count


def insert_metric_snapshots(db: Session) -> int:
    count = 0
    all_metrics = [
        {**m, "source": "simulated"} for m in METRIC_SNAPSHOTS
    ] + [
        {**m, "source": "simulated"} for m in STUDIO_METRICS
    ]

    for idx, m in enumerate(all_metrics):
        pk = sid(f"metric-{m['startup_id']}-{m['metric_name']}-{m['period_date']}-{idx}")
        if _get_or_skip(db, MetricSnapshot, pk):
            continue
        snap = MetricSnapshot(
            id=pk,
            startup_id=sid(m["startup_id"]),
            metric_name=m["metric_name"],
            value=m["value"],
            unit=m.get("unit"),
            currency=m.get("currency"),
            period_date=_d(m["period_date"]),
            period_type=PeriodType.monthly,
            source=m["source"],
        )
        db.add(snap)
        count += 1
    db.flush()
    return count


def _derive_phase(sc: dict) -> StudioPhase:
    """Derive current_studio_phase from milestone dates when not explicit."""
    if sc.get("first_external_seed_date"):
        return StudioPhase.seed
    if sc.get("pmf_date"):
        return StudioPhase.pmf
    if sc.get("mvp_date"):
        return StudioPhase.mvp
    if sc.get("validation_date"):
        return StudioPhase.validation
    return StudioPhase.idea


def insert_studio_companies(db: Session) -> int:
    count = 0

    # Portfolio startups with studio_built=True (from seed_data.py)
    for sc in PORTFOLIO_STUDIO_COMPANIES:
        pk = sid(f"sc-{sc['startup_id']}")
        if _get_or_skip(db, StudioCompany, pk):
            continue
        company = StudioCompany(
            id=pk,
            startup_id=sid(sc["startup_id"]),
            idea_date=_d(sc.get("idea_date")),
            validation_date=_d(sc.get("validation_date")),
            mvp_date=_d(sc.get("mvp_date")),
            pmf_date=_d(sc.get("pmf_date")),
            first_external_seed_date=_d(sc.get("first_external_seed_date")),
            build_cost_usd=sc.get("build_cost_usd", 0),
            equity_retained_pct=sc.get("equity_retained_pct"),
            studio_support_level=_SUPPORT_MAP[sc.get("studio_support_level", "full")],
            current_studio_phase=_derive_phase(sc),
            notes=sc.get("notes"),
        )
        db.add(company)
        count += 1

    # Pure studio startups (from studio_seed_data.py)
    for sc in STUDIO_COMPANIES:
        pk = sid(f"sc-{sc['startup_id']}")
        if _get_or_skip(db, StudioCompany, pk):
            continue
        company = StudioCompany(
            id=pk,
            startup_id=sid(sc["startup_id"]),
            idea_date=_d(sc.get("idea_date")),
            validation_date=_d(sc.get("validation_date")),
            mvp_date=_d(sc.get("mvp_date")),
            pmf_date=_d(sc.get("pmf_date")),
            first_external_seed_date=_d(sc.get("first_external_seed_date")),
            build_cost_usd=sc.get("build_cost_usd", 0),
            equity_retained_pct=sc.get("equity_retained_pct"),
            studio_support_level=_SUPPORT_MAP[sc.get("studio_support_level", "full")],
            current_studio_phase=_PHASE_MAP[sc["current_studio_phase"]],
            notes=sc.get("notes"),
        )
        db.add(company)
        count += 1

    db.flush()
    return count


def insert_studio_milestones(db: Session) -> int:
    count = 0
    for idx, m in enumerate(STUDIO_MILESTONES):
        pk = sid(f"milestone-{m['startup_id']}-{m['milestone_type']}-{idx}")
        if _get_or_skip(db, StudioMilestone, pk):
            continue
        milestone = StudioMilestone(
            id=pk,
            studio_company_id=sid(f"sc-{m['startup_id']}"),
            milestone_type=_MILESTONE_MAP[m["milestone_type"]],
            target_date=_d(m.get("target_date")),
            actual_date=_d(m.get("actual_date")),
            achieved=m.get("achieved", False),
            notes=m.get("notes"),
        )
        db.add(milestone)
        count += 1
    db.flush()
    return count


def insert_build_costs(db: Session) -> int:
    count = 0
    for idx, c in enumerate(STUDIO_BUILD_COSTS):
        pk = sid(f"cost-{c['startup_id']}-{c['cost_type']}-{idx}")
        if _get_or_skip(db, BuildCost, pk):
            continue
        cost = BuildCost(
            id=pk,
            studio_company_id=sid(f"sc-{c['startup_id']}"),
            cost_type=_COST_TYPE_MAP[c["cost_type"]],
            amount_usd=c["amount_usd"],
            period_date=_d(c["period_date"]),
            notes=c.get("notes"),
        )
        db.add(cost)
        count += 1
    db.flush()
    return count


def insert_alpha_metrics(db: Session) -> int:
    """
    Maps STUDIO_ALPHA_BENCHMARKS dict pairs into AlphaMetric rows.
    Attached to FleetOS (studio-003) as the studio's reference company.
    """
    count = 0
    ref_company_id = sid("sc-studio-003")

    alpha_pairs = [
        ("series_a_graduation_rate",  STUDIO_ALPHA_BENCHMARKS["series_a_graduation_rate_studio"],  STUDIO_ALPHA_BENCHMARKS["series_a_graduation_rate_market_latam"]),
        ("avg_months_idea_to_pmf",    STUDIO_ALPHA_BENCHMARKS["avg_months_idea_to_pmf_studio"],    STUDIO_ALPHA_BENCHMARKS["avg_months_idea_to_pmf_market"]),
        ("survival_rate_year_2",      STUDIO_ALPHA_BENCHMARKS["survival_rate_year_2_studio"],      STUDIO_ALPHA_BENCHMARKS["survival_rate_year_2_market"]),
        ("avg_build_cost_usd",        STUDIO_ALPHA_BENCHMARKS["avg_build_cost_usd"],               None),
        ("avg_external_seed_valuation", STUDIO_ALPHA_BENCHMARKS["avg_external_seed_valuation"],    None),
        ("implied_moic_on_build_cost", STUDIO_ALPHA_BENCHMARKS["implied_moic_on_build_cost"],      None),
    ]

    for metric_name, studio_val, market_val in alpha_pairs:
        pk = sid(f"alpha-{metric_name}")
        if _get_or_skip(db, AlphaMetric, pk):
            continue
        delta = None
        is_alpha = None
        if market_val is not None and market_val != 0:
            delta = round((studio_val - market_val) / market_val * 100, 4)
            is_alpha = studio_val > market_val
        metric = AlphaMetric(
            id=pk,
            studio_company_id=ref_company_id,
            metric_name=metric_name,
            studio_value=studio_val,
            market_benchmark=market_val,
            delta_pct=delta,
            is_alpha=is_alpha,
        )
        db.add(metric)
        count += 1
    db.flush()
    return count


# ── Main ──────────────────────────────────────────────────────────────────────

def load_all() -> None:
    db: Session = SessionLocal()
    try:
        print("AIDA Venture OS — Cargando seed data...")
        print("=" * 45)

        _, n = insert_fund(db)
        print(f"  funds:              {n:>4} insertados")

        n = insert_startups(db)
        print(f"  startups:           {n:>4} insertados")

        n = insert_founders(db)
        print(f"  founders:           {n:>4} insertados")

        n = insert_startup_founders(db)
        print(f"  startup_founders:   {n:>4} insertados")

        n = insert_funding_rounds(db)
        print(f"  funding_rounds:     {n:>4} insertados")

        n = insert_investments(db)
        print(f"  investments:        {n:>4} insertados")

        n = insert_metric_snapshots(db)
        print(f"  metric_snapshots:   {n:>4} insertados")

        n = insert_studio_companies(db)
        print(f"  studio_companies:   {n:>4} insertados")

        n = insert_studio_milestones(db)
        print(f"  studio_milestones:  {n:>4} insertados")

        n = insert_build_costs(db)
        print(f"  build_costs:        {n:>4} insertados")

        n = insert_alpha_metrics(db)
        print(f"  alpha_metrics:      {n:>4} insertados")

        db.commit()
        print("=" * 45)
        print("Seed data cargado correctamente.")

    except Exception as e:
        db.rollback()
        print(f"\nERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_all()
