import uuid

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.market import BenchmarkEntry, MultipleType
from app.models.startup import MetricSnapshot
from app.schemas.market import PercentileResult

# Equivalencias entre nombres de métrica y MultipleType
METRIC_TO_MULTIPLE: dict[str, MultipleType] = {
    "ARR": MultipleType.ARR,
    "MRR": MultipleType.ARR,
    "EV_Revenue": MultipleType.EV_Revenue,
}


def _interpolate_percentile(value: float, benchmarks: dict[float, float]) -> float:
    """
    Calcula la posición percentil de `value` interpolando linealmente
    entre los percentiles disponibles.

    `benchmarks` es un dict {percentil: valor_benchmark}, ej:
        {25: 1.2, 50: 2.5, 75: 4.1, 90: 7.0}

    Retorna un float entre 0 y 100.
    """
    points = sorted((pct, val) for pct, val in benchmarks.items() if val is not None)

    if not points:
        return 50.0

    # Por debajo del mínimo conocido
    if value <= points[0][1]:
        return float(points[0][0]) * value / points[0][1] if points[0][1] > 0 else 0.0

    # Por encima del máximo conocido
    if value >= points[-1][1]:
        return min(100.0, float(points[-1][0]) + (value - points[-1][1]) / points[-1][1] * 5)

    # Interpolación lineal entre los dos puntos que envuelven el valor
    for i in range(len(points) - 1):
        pct_lo, val_lo = points[i]
        pct_hi, val_hi = points[i + 1]
        if val_lo <= value <= val_hi:
            if val_hi == val_lo:
                return float(pct_lo)
            t = (value - val_lo) / (val_hi - val_lo)
            return pct_lo + t * (pct_hi - pct_lo)

    return 50.0


def calculate_percentile(
    db: Session,
    startup_id: uuid.UUID,
    metric_name: str,
    segment_id: uuid.UUID,
) -> PercentileResult:
    # 1. Último snapshot de la métrica para la startup
    snapshot = (
        db.query(MetricSnapshot)
        .filter(
            MetricSnapshot.startup_id == startup_id,
            MetricSnapshot.metric_name == metric_name,
        )
        .order_by(desc(MetricSnapshot.period_date))
        .first()
    )
    if snapshot is None:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró métrica '{metric_name}' para la startup '{startup_id}'",
        )

    # 2. Benchmark entry para el segmento y tipo de múltiplo
    multiple_type = METRIC_TO_MULTIPLE.get(metric_name)
    if multiple_type is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Métrica '{metric_name}' no tiene equivalencia en benchmarks. "
                f"Métricas soportadas: {list(METRIC_TO_MULTIPLE.keys())}"
            ),
        )

    benchmark = (
        db.query(BenchmarkEntry)
        .filter(
            BenchmarkEntry.segment_id == segment_id,
            BenchmarkEntry.multiple_type == multiple_type,
        )
        .order_by(desc(BenchmarkEntry.reference_date))
        .first()
    )
    if benchmark is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No se encontró benchmark para segment_id='{segment_id}' "
                f"y multiple_type='{multiple_type.value}'"
            ),
        )

    # 3. Calcular posición percentil por interpolación lineal
    available: dict[float, float] = {}
    if benchmark.p25 is not None:
        available[25.0] = float(benchmark.p25)
    if benchmark.p50 is not None:
        available[50.0] = float(benchmark.p50)
    if benchmark.p75 is not None:
        available[75.0] = float(benchmark.p75)
    if benchmark.p90 is not None:
        available[90.0] = float(benchmark.p90)

    value = float(snapshot.value)
    percentile_position = round(_interpolate_percentile(value, available), 2)

    # 4. Verdict
    p25 = float(benchmark.p25) if benchmark.p25 is not None else 0.0
    p50 = float(benchmark.p50) if benchmark.p50 is not None else 0.0
    p75 = float(benchmark.p75) if benchmark.p75 is not None else 0.0
    p90 = float(benchmark.p90) if benchmark.p90 is not None else 0.0

    if value > p75:
        verdict = "top_performer"
    elif value > p50:
        verdict = "above_median"
    elif value > p25:
        verdict = "below_median"
    else:
        verdict = "underperformer"

    # 5. Retornar PercentileResult
    return PercentileResult(
        startup_id=startup_id,
        metric_name=metric_name,
        value=value,
        p25=p25,
        p50=p50,
        p75=p75,
        p90=p90,
        percentile_position=percentile_position,
        verdict=verdict,
    )
