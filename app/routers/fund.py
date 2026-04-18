import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.fund import Fund, FundMetric, FundScenario, Investment
from app.schemas.fund import (
    FundMetricsRead, FundRead, FundScenarioRead, InvestmentRead,
    ScenarioInput, ScenarioResult,
)
from app.services.simulator import run_monte_carlo

router = APIRouter(prefix="/fund", tags=["fund"])


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
def simulate(inp: ScenarioInput, db: Session = Depends(get_db)):
    result = run_monte_carlo(db, inp)
    db.commit()
    return result


@router.get("/simulate/quick", response_model=ScenarioResult)
def simulate_quick(db: Session = Depends(get_db)):
    fund = _active_fund(db)
    inp = ScenarioInput(fund_id=fund.id)
    result = run_monte_carlo(db, inp)
    db.commit()
    return result
