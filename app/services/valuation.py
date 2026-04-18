import uuid

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.market import BenchmarkEntry, MultipleType
from app.models.valuation import MultipleAnalysis, ValuationEvent, ValuationVerdict
from app.schemas.valuation import MultipleAnalysisRead, ValuationAnalysisResult, ValuationEventRead

# Intenta ARR primero, luego EV_Revenue como fallback
_PREFERRED_MULTIPLES = [MultipleType.ARR, MultipleType.EV_Revenue]


def _pick_benchmark(db: Session, segment_id: uuid.UUID) -> BenchmarkEntry:
    for mtype in _PREFERRED_MULTIPLES:
        entry = (
            db.query(BenchmarkEntry)
            .filter(
                BenchmarkEntry.segment_id == segment_id,
                BenchmarkEntry.multiple_type == mtype,
            )
            .order_by(desc(BenchmarkEntry.reference_date))
            .first()
        )
        if entry is not None:
            return entry
    raise HTTPException(
        status_code=404,
        detail=f"No se encontró benchmark ARR ni EV_Revenue para segment_id='{segment_id}'",
    )


def _assign_verdict(multiple_paid: float, p25: float, p50: float, p75: float) -> ValuationVerdict:
    if multiple_paid > p75 * 2:
        return ValuationVerdict.overvalued
    if multiple_paid > p75:
        return ValuationVerdict.premium_justified
    if multiple_paid >= p25:
        return ValuationVerdict.within_range
    return ValuationVerdict.undervalued


def _build_summary(verdict: ValuationVerdict, multiple_paid: float, p50: float, premium_pct: float) -> str:
    mp = f"{multiple_paid:.1f}x"
    p50s = f"{p50:.1f}x"
    pct = f"{premium_pct:+.1f}%"
    if verdict == ValuationVerdict.within_range:
        return (
            f"Entrada disciplinada: múltiplo {mp} dentro del rango de mercado "
            f"(mediana {p50s}, diferencial {pct}). Precio consistente con la tesis."
        )
    if verdict == ValuationVerdict.premium_justified:
        return (
            f"Prima aceptable: múltiplo {mp} por encima de la mediana {p50s} ({pct}), "
            f"dentro del cuartil superior — justificable por métricas de crecimiento."
        )
    if verdict == ValuationVerdict.overvalued:
        return (
            f"Señal de alerta: múltiplo {mp} más del doble del p75 de mercado "
            f"(diferencial {pct} vs mediana {p50s}). Entrada con riesgo de sobrevaluación."
        )
    return (
        f"Entrada por debajo del mercado: múltiplo {mp} inferior al p25 "
        f"(mediana {p50s}, diferencial {pct}). Deal potencialmente subvalorado."
    )


def analyze_valuation(
    db: Session,
    startup_id: uuid.UUID,
    segment_id: uuid.UUID,
) -> ValuationAnalysisResult:
    event = (
        db.query(ValuationEvent)
        .filter(ValuationEvent.startup_id == startup_id)
        .order_by(desc(ValuationEvent.date))
        .first()
    )
    if event is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró ValuationEvent para startup_id='{startup_id}'",
        )

    if event.multiple_paid is None:
        raise HTTPException(
            status_code=422,
            detail=(
                f"El ValuationEvent más reciente de startup_id='{startup_id}' "
                "no tiene multiple_paid registrado (ronda sin ARR en ese momento)."
            ),
        )

    benchmark = _pick_benchmark(db, segment_id)

    p25 = float(benchmark.p25) if benchmark.p25 is not None else 0.0
    p50 = float(benchmark.p50) if benchmark.p50 is not None else 0.0
    p75 = float(benchmark.p75) if benchmark.p75 is not None else 0.0

    if p50 == 0:
        raise HTTPException(
            status_code=422,
            detail=f"El benchmark del segmento '{segment_id}' tiene p50=0 — no se puede calcular premium.",
        )

    multiple_paid = float(event.multiple_paid)
    premium_pct = round((multiple_paid - p50) / p50 * 100, 4)
    verdict = _assign_verdict(multiple_paid, p25, p50, p75)
    justification = _build_summary(verdict, multiple_paid, p50, premium_pct)

    analysis = MultipleAnalysis(
        valuation_event_id=event.id,
        segment_id=segment_id,
        multiple_paid=multiple_paid,
        market_p25=p25,
        market_p50=p50,
        market_p75=p75,
        premium_pct=premium_pct,
        verdict=verdict,
        justification=justification,
    )
    db.add(analysis)
    db.flush()

    return ValuationAnalysisResult(
        event=ValuationEventRead.model_validate(event),
        analysis=MultipleAnalysisRead.model_validate(analysis),
        entry_discipline_summary=justification,
    )
