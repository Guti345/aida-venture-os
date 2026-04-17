"""
AIDA Venture OS — Extended Seed Loader (Fase 2)
Inserta datos simulados para tablas vacías clave del sistema demo.
Idempotente: re-ejecutable con uuid.uuid5 deterministas.

Tablas cubiertas:
  currencies, tags, fintech_subverticals, sourcing_channels,
  deal_opportunities, thesis_alignments, dd_checklists, ic_memos,
  valuation_events

Uso: python data/load_seed_extended.py
Requiere: python data/load_seed.py ejecutado previamente
"""

import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from app.database import SessionLocal
import app.models  # noqa: F401 — registers all mappers

from app.models.shared import Currency, Tag
from app.models.fintech import FintechSubvertical, RiskLevel, RegulatoryComplexity
from app.models.dealflow import (
    SourcingChannel, DealOpportunity, ThesisAlignment, DDChecklist, ICMemo,
    SourcingChannelType, DealStatus, DDItemCategory, DDItemStatus, ICRecommendation,
)
from app.models.valuation import ValuationEvent, ValuationVerdict

# ── UUID namespace — mismo que load_seed.py para coherencia ──────────────────
_NS = uuid.UUID("a1da0000-0000-4000-8000-000000000001")

def sid(s: str) -> uuid.UUID:
    return uuid.uuid5(_NS, s)


def _get_or_skip(db: Session, model, pk):
    return db.get(model, pk)


# ── IDs derivados del seed principal (uuid.uuid5 con mismo _NS) ───────────────
# Startups
FINSTACK_ID    = sid("startup-001")   # 236cf600...
LOGIFLOW_ID    = sid("startup-002")   # 40e3bf64...
MEDISYNC_ID    = sid("startup-003")   # 947878e2...
CREDITIA_ID    = sid("startup-004")   # 0579b444...
AGRISENSE_ID   = sid("startup-005")   # 90cbcee4...

# Funding rounds (de seed_data.py — mismos strings)
ROUND_FINSTACK_PRESEED  = sid("round-001")  # FinStack Pre-Seed
ROUND_FINSTACK_SEED     = sid("round-002")  # FinStack Seed
ROUND_LOGIFLOW_SEED     = sid("round-003")  # LogiFlow Seed
ROUND_LOGIFLOW_SERIESA  = sid("round-004")  # LogiFlow Series A
ROUND_MEDISYNC_PRESEED  = sid("round-005")  # MediSync Pre-Seed
ROUND_CREDITIA_PRESEED  = sid("round-006")  # CreditIA Pre-Seed
ROUND_CREDITIA_SEED     = sid("round-007")  # CreditIA Seed
ROUND_AGRISENSE_PRESEED = sid("round-008")  # AgriSense Pre-Seed
ROUND_AGRISENSE_SEED    = sid("round-009")  # AgriSense Seed

# Segment IDs reales de la DB (Fintech Seed LATAM / SaaS Series A LATAM)
SEGMENT_FINTECH_SEED_LATAM   = uuid.UUID("cf423968-0e33-5e06-af35-67d0fc22967b")
SEGMENT_FINTECH_SERIESA_LATAM = uuid.UUID("e6299b35-2b8a-58e7-b82f-7da1dc9714ec")
SEGMENT_SAAS_SEED_LATAM      = uuid.UUID("65212ce6-aa56-51c2-831d-b9525b2b2e81")
SEGMENT_SAAS_SERIESA_LATAM   = uuid.UUID("722052fd-2597-5def-ab00-63bf7216f2bc")


# ─────────────────────────────────────────────────────────────────────────────
# 1. CURRENCIES
# ─────────────────────────────────────────────────────────────────────────────

CURRENCIES = [
    {"code": "USD", "name": "US Dollar",           "usd_fx_rate": 1.0},
    {"code": "COP", "name": "Peso Colombiano",      "usd_fx_rate": 0.000240},
    {"code": "MXN", "name": "Peso Mexicano",        "usd_fx_rate": 0.058},
    {"code": "BRL", "name": "Real Brasileño",       "usd_fx_rate": 0.195},
    {"code": "EUR", "name": "Euro",                 "usd_fx_rate": 1.085},
]


def insert_currencies(db: Session) -> int:
    count = 0
    for c in CURRENCIES:
        existing = db.get(Currency, c["code"])
        if existing:
            continue
        curr = Currency(
            code=c["code"],
            name=c["name"],
            usd_fx_rate=c["usd_fx_rate"],
            updated_at=datetime.now(timezone.utc),
        )
        db.add(curr)
        count += 1
    db.flush()
    return count


# ─────────────────────────────────────────────────────────────────────────────
# 2. TAGS
# ─────────────────────────────────────────────────────────────────────────────

TAGS = [
    {"name": "fintech",        "category": "sector",   "color_hex": "#3B82F6"},
    {"name": "saas-b2b",       "category": "modelo",   "color_hex": "#8B5CF6"},
    {"name": "logtech",        "category": "sector",   "color_hex": "#F59E0B"},
    {"name": "studio-built",   "category": "origen",   "color_hex": "#10B981"},
    {"name": "latam-colombia", "category": "geo",      "color_hex": "#FBBF24"},
    {"name": "latam-mexico",   "category": "geo",      "color_hex": "#EF4444"},
    {"name": "pre-seed",       "category": "etapa",    "color_hex": "#6B7280"},
    {"name": "seed",           "category": "etapa",    "color_hex": "#2563EB"},
    {"name": "series-a",       "category": "etapa",    "color_hex": "#7C3AED"},
    {"name": "nrr-strong",     "category": "kpi",      "color_hex": "#059669"},
    {"name": "high-growth",    "category": "kpi",      "color_hex": "#DC2626"},
    {"name": "top-performer",  "category": "status",   "color_hex": "#D97706"},
    {"name": "watchlist",      "category": "status",   "color_hex": "#9CA3AF"},
    {"name": "regulatory-risk","category": "riesgo",   "color_hex": "#B45309"},
]


def insert_tags(db: Session) -> int:
    count = 0
    for t in TAGS:
        pk = sid(f"tag-{t['name']}")
        if _get_or_skip(db, Tag, pk):
            continue
        tag = Tag(
            id=pk,
            name=t["name"],
            category=t.get("category"),
            color_hex=t.get("color_hex"),
        )
        db.add(tag)
        count += 1
    db.flush()
    return count


# ─────────────────────────────────────────────────────────────────────────────
# 3. FINTECH SUBVERTICALS
# ─────────────────────────────────────────────────────────────────────────────

FINTECH_SUBVERTICALS = [
    {
        "id": "fintechsub-payments",
        "name": "Payments",
        "description": "Infraestructura y procesamiento de pagos B2B y B2C — PSPs, agregadores, wallets.",
        "risk_level": "medium",
        "regulatory_complexity": "high",
        "key_metrics": {"take_rate_pct": 1.5, "tpv_growth_pct": 80, "chargeback_rate_pct": 0.3},
    },
    {
        "id": "fintechsub-neobanks",
        "name": "Neobanks",
        "description": "Bancos digitales sin sucursales — cuentas empresariales y personales con crédito embebido.",
        "risk_level": "high",
        "regulatory_complexity": "high",
        "key_metrics": {"cac_usd": 35, "ltv_usd": 420, "churn_monthly_pct": 2.1},
    },
    {
        "id": "fintechsub-lending",
        "name": "Lending",
        "description": "Crédito digital — BNPL, lending empresarial, scoring alternativo con ML.",
        "risk_level": "high",
        "regulatory_complexity": "high",
        "key_metrics": {"npl_pct": 4.5, "yield_pct": 28, "cac_usd": 60},
    },
    {
        "id": "fintechsub-baas",
        "name": "BaaS",
        "description": "Banking-as-a-Service — APIs bancarias para empresas no financieras. Tarjetas, cuentas, compliance.",
        "risk_level": "medium",
        "regulatory_complexity": "high",
        "key_metrics": {"api_calls_monthly": 5_000_000, "revenue_per_call_usd": 0.002},
    },
    {
        "id": "fintechsub-insurtech",
        "name": "InsurTech",
        "description": "Seguros digitales — embedded insurance, micro-seguros, distribución digital.",
        "risk_level": "medium",
        "regulatory_complexity": "medium",
        "key_metrics": {"loss_ratio_pct": 62, "combined_ratio_pct": 91, "policy_retention_pct": 78},
    },
    {
        "id": "fintechsub-wealthtech",
        "name": "WealthTech",
        "description": "Gestión de inversiones digital — robo-advisors, plataformas de inversión, savings products.",
        "risk_level": "low",
        "regulatory_complexity": "medium",
        "key_metrics": {"aum_usd": 2_500_000, "mgmt_fee_pct": 0.5, "client_retention_pct": 88},
    },
]

_RISK_MAP = {"low": RiskLevel.low, "medium": RiskLevel.medium, "high": RiskLevel.high}
_REGCOMP_MAP = {"low": RegulatoryComplexity.low, "medium": RegulatoryComplexity.medium, "high": RegulatoryComplexity.high}


def insert_fintech_subverticals(db: Session) -> int:
    count = 0
    for sv in FINTECH_SUBVERTICALS:
        pk = sid(sv["id"])
        if _get_or_skip(db, FintechSubvertical, pk):
            continue
        obj = FintechSubvertical(
            id=pk,
            name=sv["name"],
            description=sv.get("description"),
            risk_level=_RISK_MAP[sv["risk_level"]],
            regulatory_complexity=_REGCOMP_MAP[sv["regulatory_complexity"]],
            key_metrics_json=sv.get("key_metrics"),
        )
        db.add(obj)
        count += 1
    db.flush()
    return count


# ─────────────────────────────────────────────────────────────────────────────
# 4. SOURCING CHANNELS
# ─────────────────────────────────────────────────────────────────────────────

SOURCING_CHANNELS = [
    {
        "id": "sourcing-001",
        "name": "Red Alumni IESE / HBS LATAM",
        "type": "network",
        "contact_person": "Antonio Gutierrez",
        "notes": "Red de exalumnos con founders de alto perfil en LATAM.",
    },
    {
        "id": "sourcing-002",
        "name": "Rockstart LATAM Accelerator",
        "type": "accelerator",
        "contact_person": "Partnerships Rockstart",
        "notes": "Pipeline de deals post-aceleración Cohort 2023–2024.",
    },
    {
        "id": "sourcing-003",
        "name": "Demo Day Platzi Startups",
        "type": "event",
        "contact_person": None,
        "notes": "Demo days semestrales — foco ed-tech y SaaS B2B.",
    },
    {
        "id": "sourcing-004",
        "name": "Inbound — Website AIDA Ventures",
        "type": "inbound",
        "contact_person": None,
        "notes": "Aplicaciones espontáneas via formulario en el sitio web del fondo.",
    },
    {
        "id": "sourcing-005",
        "name": "Referidos de LPs del Fondo",
        "type": "network",
        "contact_person": "GPs",
        "notes": "Deals referidos directamente por inversores del fondo — alta confianza.",
    },
    {
        "id": "sourcing-006",
        "name": "Venture Studio Interno",
        "type": "studio",
        "contact_person": "Studio Operator",
        "notes": "Empresas construidas desde dentro de Scale Radical — trato preferencial.",
    },
]

_SOURCING_TYPE_MAP = {
    "network":     SourcingChannelType.network,
    "accelerator": SourcingChannelType.accelerator,
    "inbound":     SourcingChannelType.inbound,
    "studio":      SourcingChannelType.studio,
    "event":       SourcingChannelType.event,
    "cold":        SourcingChannelType.cold,
}


def insert_sourcing_channels(db: Session) -> int:
    count = 0
    for ch in SOURCING_CHANNELS:
        pk = sid(ch["id"])
        if _get_or_skip(db, SourcingChannel, pk):
            continue
        obj = SourcingChannel(
            id=pk,
            name=ch["name"],
            type=_SOURCING_TYPE_MAP[ch["type"]],
            contact_person=ch.get("contact_person"),
            active=True,
            notes=ch.get("notes"),
        )
        db.add(obj)
        count += 1
    db.flush()
    return count


# ─────────────────────────────────────────────────────────────────────────────
# 5. DEAL OPPORTUNITIES (8 deals en diferentes etapas del pipeline)
# ─────────────────────────────────────────────────────────────────────────────

DEALS = [
    # Deals invertidos (vinculados a startups del portafolio)
    {
        "id": "deal-001",
        "startup_seed_id": "startup-001",   # FinStack
        "status": "invested",
        "sourcing_id": "sourcing-001",
        "introduced_by": "Red alumni IESE",
        "identified_at": "2022-07-01",
        "screening_at": "2022-07-15",
        "dd_start_at": "2022-08-01",
        "ic_date": "2022-08-20",
        "decision": "invest",
        "decision_notes": "Equipo sólido, mercado grande, métricas de retención excepcionales para Seed.",
    },
    {
        "id": "deal-002",
        "startup_seed_id": "startup-004",   # CreditIA
        "status": "invested",
        "sourcing_id": "sourcing-006",
        "introduced_by": "Venture Studio",
        "identified_at": "2022-12-01",
        "screening_at": "2023-01-10",
        "dd_start_at": "2023-01-25",
        "ic_date": "2023-02-15",
        "decision": "invest",
        "decision_notes": "Studio co-build — riesgo reducido, control en el cap table.",
    },
    # Deal en IC (próxima decisión)
    {
        "id": "deal-003",
        "startup_seed_id": None,
        "company_name": "PayBridge CO",
        "status": "ic",
        "sourcing_id": "sourcing-005",
        "introduced_by": "LP referral — Bancolombia Ventures",
        "identified_at": "2025-09-01",
        "screening_at": "2025-09-20",
        "dd_start_at": "2025-10-15",
        "ic_date": "2025-12-01",
        "decision": None,
        "decision_notes": "Pendiente decisión IC. Fintech Payments B2B — $1.2M ARR, 180% NRR.",
    },
    # Deal en DD
    {
        "id": "deal-004",
        "startup_seed_id": None,
        "company_name": "DataRoute MX",
        "status": "dd",
        "sourcing_id": "sourcing-002",
        "introduced_by": "Rockstart LATAM Cohort 2024",
        "identified_at": "2025-10-05",
        "screening_at": "2025-10-25",
        "dd_start_at": "2025-11-10",
        "ic_date": None,
        "decision": None,
        "decision_notes": "SaaS LogTech — integración con SAP. NRR 130%, CAC payback 8 meses.",
    },
    # Deal en screening
    {
        "id": "deal-005",
        "startup_seed_id": None,
        "company_name": "GreenCredit LATAM",
        "status": "screening",
        "sourcing_id": "sourcing-004",
        "introduced_by": None,
        "identified_at": "2026-01-15",
        "screening_at": "2026-02-01",
        "dd_start_at": None,
        "ic_date": None,
        "decision": None,
        "decision_notes": "Fintech Lending verde — créditos para PYMEs con proyectos ESG.",
    },
    # Deals identificados (top del funnel)
    {
        "id": "deal-006",
        "startup_seed_id": None,
        "company_name": "InsureFlow CO",
        "status": "identified",
        "sourcing_id": "sourcing-003",
        "introduced_by": "Demo Day Q1 2026",
        "identified_at": "2026-03-10",
        "screening_at": None,
        "dd_start_at": None,
        "ic_date": None,
        "decision": None,
        "decision_notes": "InsurTech embedded — seguros de vida para gig workers. Pre-Seed.",
    },
    {
        "id": "deal-007",
        "startup_seed_id": None,
        "company_name": "WealthSimple CO",
        "status": "identified",
        "sourcing_id": "sourcing-001",
        "introduced_by": "Conexión alumni",
        "identified_at": "2026-03-20",
        "screening_at": None,
        "dd_start_at": None,
        "ic_date": None,
        "decision": None,
        "decision_notes": "WealthTech — portafolio automatizado para clase media colombiana.",
    },
    # Deal descartado
    {
        "id": "deal-008",
        "startup_seed_id": None,
        "company_name": "CryptoSav BR",
        "status": "passed",
        "sourcing_id": "sourcing-004",
        "introduced_by": None,
        "identified_at": "2025-06-01",
        "screening_at": "2025-06-20",
        "dd_start_at": None,
        "ic_date": None,
        "decision": "pass",
        "decision_notes": (
            "Modelo dependiente de crypto retail — fuera de tesis. "
            "Riesgo regulatorio alto en Brasil sin mitigación clara."
        ),
    },
]

_DEAL_STATUS_MAP = {
    "identified": DealStatus.identified,
    "screening":  DealStatus.screening,
    "dd":         DealStatus.dd,
    "ic":         DealStatus.ic,
    "invested":   DealStatus.invested,
    "passed":     DealStatus.passed,
    "watchlist":  DealStatus.watchlist,
}


def _d(s: str | None):
    return date.fromisoformat(s) if s else None


def insert_deal_opportunities(db: Session) -> int:
    count = 0
    for deal in DEALS:
        pk = sid(deal["id"])
        if _get_or_skip(db, DealOpportunity, pk):
            continue
        startup_id = sid(deal["startup_seed_id"]) if deal.get("startup_seed_id") else None
        sourcing_id = sid(deal["sourcing_id"]) if deal.get("sourcing_id") else None
        obj = DealOpportunity(
            id=pk,
            startup_id=startup_id,
            status=_DEAL_STATUS_MAP[deal["status"]],
            sourcing_channel_id=sourcing_id,
            introduced_by=deal.get("introduced_by"),
            identified_at=_d(deal["identified_at"]),
            screening_at=_d(deal.get("screening_at")),
            dd_start_at=_d(deal.get("dd_start_at")),
            ic_date=_d(deal.get("ic_date")),
            decision=deal.get("decision"),
            decision_notes=deal.get("decision_notes"),
        )
        db.add(obj)
        count += 1
    db.flush()
    return count


# ─────────────────────────────────────────────────────────────────────────────
# 6. THESIS ALIGNMENTS (scoring de tesis para deals avanzados)
# ─────────────────────────────────────────────────────────────────────────────

THESIS_ALIGNMENTS = [
    # FinStack (deal-001) — deal invertido, scoring alto
    {"id": "ta-001-team",    "deal_id": "deal-001", "dimension": "Equipo fundador",       "score": 9, "max_score": 10, "notes": "CEO ex-Rappi, CTO fintech 10+ años."},
    {"id": "ta-001-market",  "deal_id": "deal-001", "dimension": "Tamaño de mercado",     "score": 9, "max_score": 10, "notes": "PYME banking CO — $8B TAM."},
    {"id": "ta-001-product", "deal_id": "deal-001", "dimension": "Diferenciación producto","score": 8, "max_score": 10, "notes": "Cuenta + crédito embebido — ventaja vs bancos tradicionales."},
    {"id": "ta-001-thesis",  "deal_id": "deal-001", "dimension": "Alineación con tesis",  "score": 10,"max_score": 10, "notes": "Fintech B2B LATAM — core thesis."},
    # CreditIA (deal-002) — studio build
    {"id": "ta-002-team",    "deal_id": "deal-002", "dimension": "Equipo fundador",       "score": 8, "max_score": 10, "notes": "Equipo co-construido con el studio."},
    {"id": "ta-002-market",  "deal_id": "deal-002", "dimension": "Tamaño de mercado",     "score": 8, "max_score": 10, "notes": "Lending digital CO — $3B SAM."},
    {"id": "ta-002-thesis",  "deal_id": "deal-002", "dimension": "Alineación con tesis",  "score": 10,"max_score": 10, "notes": "Studio build fintech — máxima alineación."},
    # PayBridge (deal-003) — en IC
    {"id": "ta-003-team",    "deal_id": "deal-003", "dimension": "Equipo fundador",       "score": 8, "max_score": 10, "notes": "Founder ex-PayU, cofundador ex-Rappi Payments."},
    {"id": "ta-003-metrics", "deal_id": "deal-003", "dimension": "Métricas clave",        "score": 9, "max_score": 10, "notes": "NRR 180%, CAC payback 6 meses."},
    {"id": "ta-003-thesis",  "deal_id": "deal-003", "dimension": "Alineación con tesis",  "score": 9, "max_score": 10, "notes": "Payments B2B LATAM."},
]


def insert_thesis_alignments(db: Session) -> int:
    count = 0
    for ta in THESIS_ALIGNMENTS:
        pk = sid(ta["id"])
        if _get_or_skip(db, ThesisAlignment, pk):
            continue
        obj = ThesisAlignment(
            id=pk,
            deal_id=sid(ta["deal_id"]),
            thesis_dimension=ta["dimension"],
            score=ta["score"],
            max_score=ta["max_score"],
            notes=ta.get("notes"),
        )
        db.add(obj)
        count += 1
    db.flush()
    return count


# ─────────────────────────────────────────────────────────────────────────────
# 7. DD CHECKLISTS (para deals en DD o más avanzados)
# ─────────────────────────────────────────────────────────────────────────────

DD_ITEMS = [
    # DataRoute MX — deal-004 en DD
    {"id": "dd-004-team-1",   "deal_id": "deal-004", "category": "team",       "item": "Verificación background founders",      "status": "done"},
    {"id": "dd-004-team-2",   "deal_id": "deal-004", "category": "team",       "item": "Referencias de ex-empleados",           "status": "in_progress"},
    {"id": "dd-004-product-1","deal_id": "deal-004", "category": "product",    "item": "Demo técnico del producto",             "status": "done"},
    {"id": "dd-004-product-2","deal_id": "deal-004", "category": "product",    "item": "Revisión código con CTO externo",       "status": "pending"},
    {"id": "dd-004-fin-1",    "deal_id": "deal-004", "category": "financials", "item": "Auditoría estados financieros 2023–24", "status": "done"},
    {"id": "dd-004-fin-2",    "deal_id": "deal-004", "category": "financials", "item": "Proyecciones 3 años — modelo propio",   "status": "in_progress"},
    {"id": "dd-004-legal-1",  "deal_id": "deal-004", "category": "legal",      "item": "Revisión cap table y accionistas",      "status": "done"},
    {"id": "dd-004-legal-2",  "deal_id": "deal-004", "category": "legal",      "item": "Contratos clave con clientes",          "status": "pending"},
    {"id": "dd-004-market-1", "deal_id": "deal-004", "category": "market",     "item": "Análisis competitivo SAP integrations", "status": "in_progress"},
    # FinStack (deal-001) — DD completado, todo done
    {"id": "dd-001-team-1",   "deal_id": "deal-001", "category": "team",       "item": "Verificación background founders",      "status": "done"},
    {"id": "dd-001-product-1","deal_id": "deal-001", "category": "product",    "item": "Demo técnico + revisión tech stack",    "status": "done"},
    {"id": "dd-001-fin-1",    "deal_id": "deal-001", "category": "financials", "item": "Unit economics — CAC, LTV, churn",      "status": "done"},
    {"id": "dd-001-legal-1",  "deal_id": "deal-001", "category": "legal",      "item": "Cap table y acuerdos fundadores",       "status": "done"},
    {"id": "dd-001-market-1", "deal_id": "deal-001", "category": "market",     "item": "Análisis TAM/SAM/SOM Colombia",         "status": "done"},
]

_DD_CAT_MAP = {
    "team":       DDItemCategory.team,
    "product":    DDItemCategory.product,
    "market":     DDItemCategory.market,
    "financials": DDItemCategory.financials,
    "legal":      DDItemCategory.legal,
    "tech":       DDItemCategory.tech,
}

_DD_STATUS_MAP = {
    "pending":     DDItemStatus.pending,
    "in_progress": DDItemStatus.in_progress,
    "done":        DDItemStatus.done,
    "na":          DDItemStatus.na,
}


def insert_dd_checklists(db: Session) -> int:
    count = 0
    for item in DD_ITEMS:
        pk = sid(item["id"])
        if _get_or_skip(db, DDChecklist, pk):
            continue
        obj = DDChecklist(
            id=pk,
            deal_id=sid(item["deal_id"]),
            item_category=_DD_CAT_MAP[item["category"]],
            item_name=item["item"],
            status=_DD_STATUS_MAP[item["status"]],
        )
        db.add(obj)
        count += 1
    db.flush()
    return count


# ─────────────────────────────────────────────────────────────────────────────
# 8. IC MEMOS (3 memos — deals en IC o invertidos)
# ─────────────────────────────────────────────────────────────────────────────

IC_MEMOS = [
    {
        "id": "memo-001-v1",
        "deal_id": "deal-001",
        "version": 1,
        "recommendation": "invest",
        "valuation_proposed": 4_500_000,
        "key_risks": (
            "1. Riesgo regulatorio: licencia de crédito pendiente en Colombia.\n"
            "2. Competencia: neobanks regionales con más capital (Nubank, Nequi).\n"
            "3. Concentración: 3 clientes representan 40% del ARR."
        ),
        "key_upside": (
            "1. NRR 142% — retención best-in-class para Seed en LATAM.\n"
            "2. CAC payback 9 meses — eficiencia de capital superior al mercado.\n"
            "3. Equipo con track record comprobado en PayU y Rappi."
        ),
    },
    {
        "id": "memo-002-v1",
        "deal_id": "deal-002",
        "version": 1,
        "recommendation": "invest",
        "valuation_proposed": 3_500_000,
        "key_risks": (
            "1. Riesgo de originación: dependencia de scoring propio aún sin ciclo completo.\n"
            "2. NPL en entornos de estrés económico — no probado en recesión.\n"
            "3. Costo de fondeo: estructura de warehouse facility aún en negociación."
        ),
        "key_upside": (
            "1. Tasa de interés efectiva 36% — spread atractivo vs costo de fondeo.\n"
            "2. Co-build studio: equity retenido 35%, valuation de entrada bajo.\n"
            "3. Pipeline B2B: 45 empresas en lista de espera."
        ),
    },
    {
        "id": "memo-003-v1",
        "deal_id": "deal-003",
        "version": 1,
        "recommendation": "invest",
        "valuation_proposed": 7_000_000,
        "key_risks": (
            "1. Valuación alta para Seed LATAM — múltiplo ARR 5.8x vs mediana 4.2x.\n"
            "2. Competencia de PayU y Kushki con más recursos.\n"
            "3. Dependencia de 2 integraciones bancarias críticas."
        ),
        "key_upside": (
            "1. NRR 180% — mejor en clase para Payments B2B en LATAM.\n"
            "2. Referido por LP estratégico (Bancolombia Ventures) — acceso a pipeline bancario.\n"
            "3. Expansión México Q3 2026 — mercado 5x mayor que Colombia."
        ),
    },
]

_IC_REC_MAP = {
    "invest":    ICRecommendation.invest,
    "pass":      ICRecommendation.pass_,
    "watchlist": ICRecommendation.watchlist,
}


def insert_ic_memos(db: Session) -> int:
    count = 0
    for memo in IC_MEMOS:
        pk = sid(memo["id"])
        if _get_or_skip(db, ICMemo, pk):
            continue
        obj = ICMemo(
            id=pk,
            deal_id=sid(memo["deal_id"]),
            version=memo["version"],
            recommendation=_IC_REC_MAP[memo["recommendation"]],
            valuation_proposed=memo.get("valuation_proposed"),
            key_risks=memo.get("key_risks"),
            key_upside=memo.get("key_upside"),
            created_at=datetime.now(timezone.utc),
        )
        db.add(obj)
        count += 1
    db.flush()
    return count


# ─────────────────────────────────────────────────────────────────────────────
# 9. VALUATION EVENTS (uno por cada ronda de inversión existente)
# ─────────────────────────────────────────────────────────────────────────────
# IDs de rondas (de seed_data.py):
#   round-001 FinStack Pre-Seed  → pre_money $500K,  ARR ~$0 (pre-revenue)
#   round-002 FinStack Seed      → pre_money $4.5M,  ARR $480K
#   round-003 LogiFlow Seed      → pre_money $5.0M,  ARR $650K
#   round-004 LogiFlow Series A  → pre_money $18.0M, ARR $3.2M
#   round-005 MediSync Pre-Seed  → pre_money $800K,  ARR $36K
#   round-006 CreditIA Pre-Seed  → pre_money $600K,  ARR $0
#   round-007 CreditIA Seed      → pre_money $4.0M,  ARR $620K
#   round-008 AgriSense Pre-Seed → pre_money $1.2M,  ARR $0
#   round-009 AgriSense Seed     → pre_money $4.5M,  ARR $390K

VALUATION_EVENTS_DATA = [
    {
        "id": "ve-001",
        "startup_seed_id": "startup-001",
        "round_seed_id": "r-001",
        "pre_money_val": 1_500_000,
        "arr_at_time": None,
        "multiple_paid": None,
        "segment_id": SEGMENT_FINTECH_SEED_LATAM,
        "date": "2022-09-01",
    },
    {
        "id": "ve-002",
        "startup_seed_id": "startup-001",
        "round_seed_id": "r-002",
        "pre_money_val": 6_000_000,
        "arr_at_time": 480_000,
        "multiple_paid": 12.5,
        "segment_id": SEGMENT_FINTECH_SEED_LATAM,
        "date": "2023-06-15",
    },
    {
        "id": "ve-003",
        "startup_seed_id": "startup-002",
        "round_seed_id": "r-003",
        "pre_money_val": 7_500_000,
        "arr_at_time": 650_000,
        "multiple_paid": 11.54,
        "segment_id": SEGMENT_SAAS_SEED_LATAM,
        "date": "2022-02-01",
    },
    {
        "id": "ve-004",
        "startup_seed_id": "startup-002",
        "round_seed_id": "r-004",
        "pre_money_val": 22_000_000,
        "arr_at_time": 3_200_000,
        "multiple_paid": 6.875,
        "segment_id": SEGMENT_SAAS_SERIESA_LATAM,
        "date": "2023-11-01",
    },
    {
        "id": "ve-005",
        "startup_seed_id": "startup-003",
        "round_seed_id": "r-005",
        "pre_money_val": 1_200_000,
        "arr_at_time": 36_000,
        "multiple_paid": 33.3,
        "segment_id": SEGMENT_SAAS_SEED_LATAM,
        "date": "2023-12-01",
    },
    {
        "id": "ve-006",
        "startup_seed_id": "startup-004",
        "round_seed_id": "r-006",
        "pre_money_val": 1_800_000,
        "arr_at_time": None,
        "multiple_paid": None,
        "segment_id": SEGMENT_FINTECH_SEED_LATAM,
        "date": "2023-03-01",
    },
    {
        "id": "ve-007",
        "startup_seed_id": "startup-004",
        "round_seed_id": "r-007",
        "pre_money_val": 5_500_000,
        "arr_at_time": 620_000,
        "multiple_paid": 8.87,
        "segment_id": SEGMENT_FINTECH_SEED_LATAM,
        "date": "2024-01-15",
    },
    {
        "id": "ve-008",
        "startup_seed_id": "startup-005",
        "round_seed_id": "r-008",
        "pre_money_val": 2_000_000,
        "arr_at_time": None,
        "multiple_paid": None,
        "segment_id": SEGMENT_SAAS_SEED_LATAM,
        "date": "2022-11-01",
    },
    {
        "id": "ve-009",
        "startup_seed_id": "startup-005",
        "round_seed_id": "r-009",
        "pre_money_val": 7_000_000,
        "arr_at_time": 390_000,
        "multiple_paid": 17.95,
        "segment_id": SEGMENT_SAAS_SEED_LATAM,
        "date": "2024-03-01",
    },
]


def insert_valuation_events(db: Session) -> int:
    count = 0
    for ve in VALUATION_EVENTS_DATA:
        pk = sid(ve["id"])
        if _get_or_skip(db, ValuationEvent, pk):
            continue
        obj = ValuationEvent(
            id=pk,
            startup_id=sid(ve["startup_seed_id"]),
            round_id=sid(ve["round_seed_id"]),
            pre_money_val=ve["pre_money_val"],
            arr_at_time=ve.get("arr_at_time"),
            multiple_paid=ve.get("multiple_paid"),
            segment_id=ve.get("segment_id"),
            date=_d(ve["date"]),
        )
        db.add(obj)
        count += 1
    db.flush()
    return count


# ── Main ──────────────────────────────────────────────────────────────────────

def load_extended() -> None:
    db: Session = SessionLocal()
    try:
        print("AIDA Venture OS — Cargando seed data extendida (Fase 2)...")
        print("=" * 52)

        n = insert_currencies(db)
        print(f"  currencies:             {n:>4} insertadas")

        n = insert_tags(db)
        print(f"  tags:                   {n:>4} insertados")

        n = insert_fintech_subverticals(db)
        print(f"  fintech_subverticals:   {n:>4} insertados")

        n = insert_sourcing_channels(db)
        print(f"  sourcing_channels:      {n:>4} insertados")

        n = insert_deal_opportunities(db)
        print(f"  deal_opportunities:     {n:>4} insertados")

        n = insert_thesis_alignments(db)
        print(f"  thesis_alignments:      {n:>4} insertados")

        n = insert_dd_checklists(db)
        print(f"  dd_checklists:          {n:>4} insertados")

        n = insert_ic_memos(db)
        print(f"  ic_memos:               {n:>4} insertados")

        n = insert_valuation_events(db)
        print(f"  valuation_events:       {n:>4} insertados")

        db.commit()
        print("=" * 52)
        print("Seed extendida cargada correctamente.")

    except Exception as e:
        db.rollback()
        print(f"\nERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_extended()
