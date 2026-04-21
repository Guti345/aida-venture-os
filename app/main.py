from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.routers import auth, fintech, fund, market, reporting, startups, studio, valuation
from app.routers.dealflow import router_deals, router_sourcing
from app.services.auth import require_analyst, require_gp

app = FastAPI(
    title="AIDA Venture OS",
    version="0.1.0",
    description=(
        "Sistema operativo de decisión para venture capital y venture studio — "
        "AIDA Ventures + Scale Radical. "
        "Convierte datos dispersos en decisiones comparables, auditables y reproducibles."
    ),
)


@app.get("/")
def root():
    return {
        "sistema": "AIDA Venture OS",
        "version": "0.1.0",
        "estado": "operativo",
        "modo": "demo — datos 100% simulados",
        "docs": "/docs",
    }


app.include_router(auth.router)
app.include_router(startups.router)
app.include_router(market.router)
app.include_router(valuation.router)
app.include_router(fund.router)
app.include_router(studio.router)
app.include_router(fintech.router)
app.include_router(router_deals)
app.include_router(router_sourcing)
app.include_router(reporting.router)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "base_de_datos": "conectada",
    }
