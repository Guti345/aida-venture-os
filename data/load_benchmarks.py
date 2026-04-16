"""
AIDA Venture OS — Benchmark Loader
Lee 4 archivos Excel de data/ y carga market_segments + benchmark_entries en PostgreSQL.
Idempotente: re-ejecutable sin errores si los registros ya existen.

Archivos:
  _Metricas Startups.xlsx          — benchmarks SaaS por etapa (US)
  _AIDA Ventures - Startups Benchmarks.xlsx — múltiplos por sector/etapa/geografía
  VCFunds Metrics.xlsx             — métricas de fondos early-stage
  Fintech Sectors.xlsx             — inversión por subsector Fintech LATAM/USA

Uso: python data/load_benchmarks.py
"""
import re
import sys
import uuid
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from sqlalchemy.orm import Session

from app.database import SessionLocal
import app.models  # noqa: F401 — registra todos los mappers en Base.metadata

from app.models.market import BenchmarkEntry, MarketSegment, MarketStage, MultipleType

DATA_DIR = Path(__file__).parent

# Namespace separado del seed data para no colisionar UUIDs
_NS = uuid.UUID("a1da0000-0000-4000-8000-000000000002")


def sid(key: str) -> uuid.UUID:
    return uuid.uuid5(_NS, key)


# ── Mapas de conversión ───────────────────────────────────────────────────────

_STAGE_MAP: dict[str, MarketStage] = {
    "pre-seed":  MarketStage.pre_seed,
    "pre seed":  MarketStage.pre_seed,
    "preseed":   MarketStage.pre_seed,
    "seed":      MarketStage.seed,
    "serie a":   MarketStage.series_a,
    "series a":  MarketStage.series_a,
    "series_a":  MarketStage.series_a,
    "serie b":   MarketStage.series_b,
    "series b":  MarketStage.series_b,
    "series_b":  MarketStage.series_b,
}

_MULTIPLE_MAP: dict[str, MultipleType] = {
    "arr":         MultipleType.ARR,
    "mrr":         MultipleType.ARR,
    "revenue/arr": MultipleType.ARR,
    "ev/revenue":  MultipleType.EV_Revenue,
    "ev_revenue":  MultipleType.EV_Revenue,
    "ev revenue":  MultipleType.EV_Revenue,
    "revenue":     MultipleType.EV_Revenue,
    "ebitda":      MultipleType.EBITDA,
    "gmv":         MultipleType.GMV,
    # Métricas de fondo — multiples de retorno se mapean al tipo más cercano
    "tvpi":        MultipleType.ARR,
    "moic":        MultipleType.ARR,
    "dpi":         MultipleType.ARR,
    "irr":         MultipleType.ARR,
}


# ── Parser de rangos numéricos ────────────────────────────────────────────────

def _to_float(s: str) -> float | None:
    """Convierte un token numérico ("$5.27M", "12x", "~30%") a float."""
    s = s.strip().replace(",", "").replace("+", "")
    mult = 1.0
    up = s.upper()
    if up.endswith("B"):
        mult = 1e9
        s = s[:-1]
    elif up.endswith("M"):
        mult = 1e6
        s = s[:-1]
    elif up.endswith("K"):
        mult = 1e3
        s = s[:-1]
    s = re.sub(r"[~$%x×]", "", s).strip()
    try:
        v = float(s) * mult
        return v if v >= 0 else None
    except ValueError:
        return None


def _parse_range(
    text,
) -> tuple[float | None, float | None, float | None] | None:
    """
    Extrae (p25, p50, p75) de texto como "8–12x", "$100K–$1M", "~$500K".

    - Valor único  → (None, valor, None)
    - Dos valores  → (bajo, punto_medio, alto)
    - Sin contenido numérico → None
    """
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None
    text = str(text).strip()
    if not text or text.lower() in ("n/a", "—", "–", "-", "nan", ""):
        return None

    # Eliminar aclaraciones entre paréntesis ("mediana ~$500K", "2025", etc.)
    text = re.sub(r"\([^)]*\)", "", text)
    # Normalizar guiones (en-dash, em-dash → hyphen)
    text = text.replace("–", "-").replace("—", " ")

    # Extraer tokens numéricos: prefijo opcional ~$, dígitos, sufijo K/M/B, unidad %/x
    tokens = re.findall(r"[~$]*[\d,]+\.?\d*[KMBkmb]?[%x]?", text)
    nums: list[float] = []
    for t in tokens:
        v = _to_float(t)
        if v is not None:
            nums.append(v)

    if not nums:
        return None
    if len(nums) == 1:
        return (None, nums[0], None)
    # Toma los dos primeros valores como rango IQR
    lo, hi = nums[0], nums[1]
    return (lo, (lo + hi) / 2, hi)


def _cell_str(val) -> str:
    """Convierte celda de pandas a str limpio, empty string si NaN."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    return str(val).strip()


# ── Helpers de base de datos ──────────────────────────────────────────────────

def _get_or_create_segment(
    db: Session,
    sector: str,
    stage: MarketStage,
    geography: str,
    country: str | None = None,
    subsector: str | None = None,
) -> tuple[MarketSegment, bool]:
    """Retorna (segmento, es_nuevo). Crea solo si no existe."""
    key = f"seg:{sector}:{subsector or ''}:{stage.value}:{geography}:{country or ''}"
    pk = sid(key)
    existing = db.get(MarketSegment, pk)
    if existing:
        return existing, False
    seg = MarketSegment(
        id=pk,
        sector=sector,
        subsector=subsector,
        stage=stage,
        geography=geography,
        country=country,
    )
    db.add(seg)
    db.flush()
    return seg, True


def _add_entry(
    db: Session,
    key: str,
    segment: MarketSegment,
    multiple_type: MultipleType,
    parsed: tuple[float | None, float | None, float | None],
    ref_date: date,
    source: str,
    notes: str | None = None,
) -> bool:
    """Inserta BenchmarkEntry si no existe. Retorna True si fue insertado."""
    pk = sid(key)
    if db.get(BenchmarkEntry, pk):
        return False
    p25, p50, p75 = parsed
    db.add(BenchmarkEntry(
        id=pk,
        segment_id=segment.id,
        multiple_type=multiple_type,
        p10=None,
        p25=p25,
        p50=p50,
        p75=p75,
        p90=None,
        reference_date=ref_date,
        source=source,
        notes=notes,
    ))
    return True


# ── Loader 1: _Metricas Startups.xlsx ────────────────────────────────────────

def load_metricas_startups(db: Session) -> tuple[int, int]:
    """
    Carga benchmarks de startups SaaS por etapa desde 4 hojas.
    Segmentos: sector=SaaS, geography=US.
    """
    path = DATA_DIR / "_Metricas Startups.xlsx"
    n_seg = n_ent = 0

    # (sheet_name, metric_substring, multiple_type, notes_label)
    targets = [
        ("Income&Growth US",    "ARR (Annual",            MultipleType.ARR,         "ARR USD target range by stage"),
        ("Income&Growth US",    "MRR (Monthly",           MultipleType.ARR,         "MRR USD target range by stage"),
        ("Market&Valuation",    "ltiplo ARR",             MultipleType.ARR,         "ARR valuation multiple"),
        ("Market&Valuation",    "Valuaci",                MultipleType.EV_Revenue,  "Pre-money valuation USD median"),
        ("Capital Efficiency US", "Capital total levantado", MultipleType.EV_Revenue, "Round size USD by stage"),
        ("Unit Economics",      "Gross Margin",           MultipleType.EBITDA,      "Gross margin % by stage"),
    ]

    # Col indices → (stage_key, geography)
    stage_cols = {2: "pre-seed", 3: "seed", 4: "serie a"}
    ref_date = date(2025, 1, 1)
    source = "_Metricas Startups.xlsx"

    for sheet_name, metric_substr, multiple_type, notes_label in targets:
        try:
            df = pd.read_excel(path, sheet_name=sheet_name, header=None)
        except Exception as e:
            print(f"    ! No se pudo leer '{sheet_name}': {e}")
            continue

        for _, row in df.iterrows():
            cell1 = _cell_str(row.iloc[1]) if len(row) > 1 else ""
            if metric_substr.lower() not in cell1.lower():
                continue

            for col_idx, stage_str in stage_cols.items():
                if col_idx >= len(row):
                    continue
                raw_val = row.iloc[col_idx]
                parsed = _parse_range(raw_val)
                if parsed is None:
                    continue

                stage = _STAGE_MAP[stage_str]
                seg, is_new = _get_or_create_segment(db, "SaaS", stage, "US")
                if is_new:
                    n_seg += 1

                entry_key = f"metricas:{sheet_name}:{metric_substr}:{stage_str}"
                if _add_entry(
                    db, entry_key, seg, multiple_type, parsed, ref_date,
                    source, f"{notes_label} — {_cell_str(raw_val)[:120]}",
                ):
                    n_ent += 1
            break  # métrica encontrada, siguiente target

    return n_seg, n_ent


# ── Loader 2: _AIDA Ventures - Startups Benchmarks.xlsx ──────────────────────

def load_aida_benchmarks(db: Session) -> tuple[int, int]:
    """
    Carga múltiplos de revenue por sector/etapa desde la hoja 'Revenue Multiples'.
    Crea entradas separadas para Global y LATAM.
    """
    path = DATA_DIR / "_AIDA Ventures - Startups Benchmarks.xlsx"
    df = pd.read_excel(path, sheet_name="Revenue Multiples", header=None)

    n_seg = n_ent = 0
    current_sector: str | None = None
    ref_date = date(2025, 1, 1)

    for _, row in df.iterrows():
        cell0 = _cell_str(row.iloc[0])

        # Encabezado de sección: "▸  SaaS / Enterprise Software — ARR Multiples"
        if "▸" in cell0:
            if "SaaS" in cell0 or "Enterprise" in cell0:
                current_sector = "SaaS"
            elif "Fintech" in cell0:
                current_sector = "Fintech"
            elif "LogTech" in cell0 or "Supply Chain" in cell0:
                current_sector = "LogTech"
            else:
                current_sector = cell0.replace("▸", "").split("—")[0].strip()
            continue

        # Saltar filas de encabezado de columnas y vacías
        if not current_sector or cell0.lower() in ("", "nan", "stage"):
            continue

        stage = _STAGE_MAP.get(cell0.lower())
        if stage is None:
            continue  # Late Growth, Public Comps, M&A Exit → fuera de nuestro enum

        # Tipo de múltiplo (col 1)
        mult_text = _cell_str(row.iloc[1]).lower() if len(row) > 1 else ""
        multiple_type = _MULTIPLE_MAP.get(mult_text, MultipleType.ARR)

        # Fuente (col 5) y notas (col 7)
        source_raw = _cell_str(row.iloc[5]) if len(row) > 5 else ""
        source = source_raw if source_raw and source_raw != "nan" \
            else "AIDA Ventures Benchmarks"
        notes_raw = _cell_str(row.iloc[7]) if len(row) > 7 else ""
        notes = notes_raw if notes_raw and notes_raw != "nan" else None

        for geo, col_idx in [("Global", 2), ("LATAM", 3)]:
            raw_val = row.iloc[col_idx] if len(row) > col_idx else None
            parsed = _parse_range(raw_val)
            if parsed is None:
                continue

            seg, is_new = _get_or_create_segment(db, current_sector, stage, geo)
            if is_new:
                n_seg += 1

            entry_key = (
                f"aida:rev:{current_sector}:{stage.value}"
                f":{multiple_type.value}:{geo}"
            )
            if _add_entry(
                db, entry_key, seg, multiple_type, parsed,
                ref_date, source, notes,
            ):
                n_ent += 1

    return n_seg, n_ent


# ── Loader 3: VCFunds Metrics.xlsx ───────────────────────────────────────────

def load_vcfunds_metrics(db: Session) -> tuple[int, int]:
    """
    Carga benchmarks de fondos VC early-stage.
    Hoja EarlyStageFunds: por etapa (Pre-Seed / Seed / Serie A).
    Hoja LATAM vs US: comparativa geográfica, stage=Seed como representativo.
    MultipleType.ARR se usa para TVPI/MOIC/DPI (todos son múltiplos de retorno).
    """
    path = DATA_DIR / "VCFunds Metrics.xlsx"
    n_seg = n_ent = 0
    ref_date = date(2025, 1, 1)
    source = "VCFunds Metrics.xlsx"

    # Palabras clave → tipo de múltiplo
    metric_keywords = {
        "tvpi":  MultipleType.ARR,
        "moic":  MultipleType.ARR,
        "dpi":   MultipleType.ARR,
        "irr":   MultipleType.ARR,
        "ticket": MultipleType.EV_Revenue,
        "tamaño": MultipleType.EV_Revenue,
        "valuaci": MultipleType.EV_Revenue,
    }

    # ── EarlyStageFunds: columnas Pre-Seed (2), Seed (3), Serie A (4) ──────
    df = pd.read_excel(path, sheet_name="EarlyStageFunds", header=None)
    stage_cols = {2: MarketStage.pre_seed, 3: MarketStage.seed, 4: MarketStage.series_a}

    for _, row in df.iterrows():
        cell = _cell_str(row.iloc[1]).lower() if len(row) > 1 else ""
        if not cell or cell in ("métrica", "nan"):
            continue

        mtype = next(
            (v for k, v in metric_keywords.items() if k in cell),
            None,
        )
        if mtype is None:
            continue

        for col_idx, stage in stage_cols.items():
            if col_idx >= len(row):
                continue
            parsed = _parse_range(row.iloc[col_idx])
            if parsed is None:
                continue

            seg, is_new = _get_or_create_segment(db, "VC Fund", stage, "Global")
            if is_new:
                n_seg += 1

            entry_key = f"vcfund:early:{cell[:50]}:{stage.value}"
            if _add_entry(
                db, entry_key, seg, mtype, parsed, ref_date, source,
                f"Fondo early-stage — {cell}",
            ):
                n_ent += 1

    # ── LATAM vs US: col 2 = EE.UU., col 3 = LATAM; stage=Seed ───────────
    df2 = pd.read_excel(path, sheet_name="LATAM vs US", header=None)
    geo_cols = {2: ("US", None), 3: ("LATAM", None)}

    for _, row in df2.iterrows():
        cell = _cell_str(row.iloc[1]).lower() if len(row) > 1 else ""
        if not cell or cell in ("métrica", "nan"):
            continue

        mtype = next(
            (v for k, v in metric_keywords.items() if k in cell),
            None,
        )
        if mtype is None:
            continue

        for col_idx, (geo, country) in geo_cols.items():
            if col_idx >= len(row):
                continue
            parsed = _parse_range(row.iloc[col_idx])
            if parsed is None:
                continue

            seg, is_new = _get_or_create_segment(
                db, "VC Fund", MarketStage.seed, geo, country=country
            )
            if is_new:
                n_seg += 1

            entry_key = f"vcfund:latamvs:{cell[:50]}:{geo}"
            if _add_entry(
                db, entry_key, seg, mtype, parsed, ref_date, source,
                f"LATAM vs US early-stage — {cell}",
            ):
                n_ent += 1

    return n_seg, n_ent


# ── Loader 4: Fintech Sectors.xlsx ───────────────────────────────────────────

def load_fintech_sectors(db: Session) -> tuple[int, int]:
    """
    Carga benchmarks de inversión por subsector Fintech.
    Hoja LATAM Subsectors 2024 y USA Subsectors 2024.
    Los montos de inversión se cargan como proxy GMV (tamaño de mercado).
    Stage=Seed como representativo del ecosistema.
    """
    path = DATA_DIR / "Fintech Sectors.xlsx"
    n_seg = n_ent = 0

    sheets = [
        ("LATAM Subsectors 2024", "LATAM", None),
        ("USA Subsectors 2024",   "US",    "US"),
    ]

    for sheet_name, geography, country in sheets:
        try:
            df = pd.read_excel(path, sheet_name=sheet_name, header=None)
        except Exception as e:
            print(f"    ! No se pudo leer '{sheet_name}': {e}")
            continue

        for _, row in df.iterrows():
            subsector = _cell_str(row.iloc[0])
            if not subsector or subsector.lower() in ("nan", "subsector"):
                continue

            # Col 1 = monto de inversión 2024
            raw_val = row.iloc[1] if len(row) > 1 else None
            parsed = _parse_range(raw_val)
            if parsed is None:
                continue

            seg, is_new = _get_or_create_segment(
                db, "Fintech", MarketStage.seed, geography,
                country=country, subsector=subsector,
            )
            if is_new:
                n_seg += 1

            entry_key = f"fintech:{geography}:{subsector}:investment_2024"
            if _add_entry(
                db, entry_key, seg, MultipleType.GMV, parsed,
                date(2024, 1, 1),
                f"Fintech Sectors.xlsx — {sheet_name}",
                f"Inversión total subsector Fintech {geography} 2024 USD",
            ):
                n_ent += 1

    return n_seg, n_ent


# ── Main ──────────────────────────────────────────────────────────────────────

def load_all() -> None:
    db: Session = SessionLocal()
    try:
        print("AIDA Venture OS — Cargando benchmarks desde Excel...")
        print("=" * 52)

        total_seg = total_ent = 0

        loaders = [
            (load_metricas_startups,  "_Metricas Startups.xlsx"),
            (load_aida_benchmarks,    "_AIDA Ventures - Startups Benchmarks.xlsx"),
            (load_vcfunds_metrics,    "VCFunds Metrics.xlsx"),
            (load_fintech_sectors,    "Fintech Sectors.xlsx"),
        ]

        for loader_fn, filename in loaders:
            n_seg, n_ent = loader_fn(db)
            total_seg += n_seg
            total_ent += n_ent
            print(f"  {filename}")
            print(f"    market_segments:   {n_seg:>4} insertados")
            print(f"    benchmark_entries: {n_ent:>4} insertados")

        db.commit()
        print("=" * 52)
        print(f"  TOTAL market_segments:   {total_seg:>4}")
        print(f"  TOTAL benchmark_entries: {total_ent:>4}")
        print("Benchmarks cargados correctamente.")

    except Exception as e:
        db.rollback()
        print(f"\nERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_all()
