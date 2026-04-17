# CLAUDE.md — Memoria del proyecto AIDA Venture OS

Este archivo es leído automáticamente por Claude Code en cada sesión.
Contiene todo el contexto necesario para continuar el desarrollo sin repetir instrucciones.

---

## Identidad del proyecto

**Nombre:** AIDA Venture OS  
**Descripción:** Sistema operativo de decisión para venture capital y venture studio.  
**Empresa:** AIDA Ventures + Scale Radical  
**Estado actual:** Fase 1 completa — Motor de comparabilidad operativo con 503 registros en DB  
**Objetivo inmediato:** Fase 2 — Valuation Intel, Fund Simulator Monte Carlo, Studio router  

---

## Stack tecnológico

| Componente | Tecnología | Versión |
|---|---|---|
| Lenguaje | Python | 3.14 |
| Framework | FastAPI + Uvicorn | Latest |
| Base de datos | PostgreSQL | 18 — local, puerto 5432 |
| ORM | SQLAlchemy | 2.x — API declarativa con Mapped[] |
| Migraciones | Alembic | Latest |
| Validación | Pydantic | v2 |
| Procesamiento | Pandas + NumPy + SciPy | Latest |
| Entorno | virtualenv (venv) | Python 3.14 |

---

## Estructura de carpetas

```
aida-venture-os/
├── app/
│   ├── main.py              ✅ FastAPI entry point — routers startups + market registrados
│   ├── database.py          ✅ Conexión PostgreSQL con SQLAlchemy
│   ├── models/
│   │   ├── __init__.py      ✅ Importaciones ordenadas por grafo FK
│   │   ├── shared.py        ✅ users, currencies, tags, audit_logs
│   │   ├── startup.py       ✅ startups, founders, startup_founders, funding_rounds, metric_snapshots
│   │   ├── market.py        ✅ market_segments, benchmark_entries, benchmark_series, valuation_distributions
│   │   ├── valuation.py     ✅ valuation_events, multiple_analyses, valuation_drivers, outlier_flags
│   │   ├── fund.py          ✅ funds, lps, investments, fund_scenarios, fund_metrics
│   │   ├── studio.py        ✅ studio_companies, build_costs, studio_milestones, alpha_metrics
│   │   ├── fintech.py       ✅ fintech_subverticals, fintech_unit_economics, regulatory_risks, fintech_comparables
│   │   ├── dealflow.py      ✅ deal_opportunities, thesis_alignments, sourcing_channels, dd_checklists, ic_memos
│   │   └── reporting.py     ✅ lp_profiles, reports, narrative_blocks, ic_decisions
│   ├── schemas/
│   │   ├── startup.py       ✅ StartupList, StartupRead, StartupWithMetrics, MetricSnapshotRead
│   │   └── market.py        ✅ MarketSegmentRead, BenchmarkEntryRead, PercentileResult
│   ├── routers/
│   │   ├── startups.py      ✅ 5 endpoints — lista, detalle, métricas, percentil, latest
│   │   └── market.py        ✅ 2 endpoints — segmentos y benchmarks con filtros
│   └── services/
│       ├── percentile.py    ✅ Cálculo de percentiles con interpolación lineal
│       ├── simulator.py     ⬜ PENDIENTE — Monte Carlo MOIC/IRR
│       ├── alpha.py         ⬜ PENDIENTE — Studio alpha vs mercado
│       └── importer.py      ⬜ PENDIENTE — Importación de Excels a DB
├── alembic/                 ✅ Migraciones configuradas — 43 tablas en producción
├── data/
│   ├── seed_data.py         ✅ 5 startups portafolio + fondo (147 registros)
│   ├── studio_seed_data.py  ✅ 5 empresas venture studio (95 registros)
│   ├── load_seed.py         ✅ Cargador unificado idempotente — 255 registros
│   ├── load_benchmarks.py   ✅ Benchmarks desde Excels — 54 segmentos + 119 benchmarks
│   ├── load_seed_extended.py ✅ Seed extendida Fase 2 — 75 registros adicionales
│   └── *.xlsx               ✅ 5 archivos de benchmarks externos
├── tests/                   ⬜ PENDIENTE — carpeta vacía
├── .env                     ✅ Credenciales locales (no en GitHub)
├── .env.example             ✅ Template público
├── requirements.txt         ✅
├── README.md                ✅
└── CLAUDE.md                ✅ ESTE ARCHIVO
```

---

## Base de datos

**Nombre:** `aida_venture_os`  
**Usuario:** `postgres`  
**Puerto:** `5432`  
**Host:** `localhost`  
**Connection string:** en `.env` como `DATABASE_URL`

### 43 tablas en 8 dominios — estado al 2026-04-17

| Dominio | Tablas | Modelo | Seed data | Registros |
|---|---|---|---|---|
| Transversales | users, currencies, tags, audit_logs | ✅ | 🔄 parcial | 19 (currencies 5, tags 14) |
| Startup Engine | startups, founders, startup_founders, funding_rounds, metric_snapshots | ✅ | ✅ | 197 |
| Market Reality | market_segments, benchmark_entries, benchmark_series, valuation_distributions | ✅ | ✅ | 173 |
| Valuation Intel | valuation_events, multiple_analyses, valuation_drivers, outlier_flags | ✅ | 🔄 parcial | 9 (solo valuation_events) |
| Fund Simulator | funds, lps, investments, fund_scenarios, fund_metrics | ✅ | 🔄 parcial | 10 (fund 1, investments 9) |
| Studio Performance | studio_companies, build_costs, studio_milestones, alpha_metrics | ✅ | ✅ | 48 |
| Fintech Deep Dive | fintech_subverticals, fintech_unit_economics, regulatory_risks, fintech_comparables | ✅ | 🔄 parcial | 6 (solo subverticals) |
| Deal Flow | deal_opportunities, thesis_alignments, sourcing_channels, dd_checklists, ic_memos | ✅ | ✅ | 41 |
| Reporting | lp_profiles, reports, narrative_blocks, ic_decisions | ✅ | ⬜ | 0 |
| **TOTAL** | | | | **503** |

---

## Convenciones de código — SEGUIR SIEMPRE

### SQLAlchemy
- Usar siempre la API declarativa moderna con `Mapped[]` y `mapped_column()`
- UUIDs con `UUID(as_uuid=True)` — nunca strings
- Timestamps con `DateTime(timezone=True)` — siempre con zona horaria
- Enums definidos como `PyEnum` en Python con nombre explícito en PostgreSQL
- JSONB para campos de datos semiestructurados (no JSON simple)
- Relaciones con `relationship()` y `back_populates`

### FastAPI
- Cada dominio tiene su propio router en `app/routers/`
- Cada endpoint tiene su schema Pydantic en `app/schemas/`
- Dependencia de DB siempre via `Depends(get_db)`
- Respuestas tipadas con modelos Pydantic v2

### General
- Nunca hardcodear credenciales — siempre desde `.env`
- Nunca hardcodear el tamaño del fondo — siempre desde `FUND_TARGET_SIZE_USD` en `.env`
- Toda métrica tiene `period_date` y `source` — sin excepción
- No promedios — siempre percentiles (p25, p50, p75, p90)
- Campo `is_simulated: bool` en startups para distinguir datos reales de simulados
- Commits atómicos: un commit = una funcionalidad completa

---

## Roles de usuario

| Rol | Acceso |
|---|---|
| `gp` | Total — todas las vistas y configuración |
| `analyst` | Lectura + entrada de datos — sin simulador ni config del fondo |
| `studio_operator` | Solo empresas del venture studio |
| `viewer` | Solo lectura — para LPs |

---

## Datos simulados disponibles

### data/seed_data.py — Portafolio externo (147 registros)
- **FinStack** — Fintech Neobank B2B — Seed — Colombia — ARR $480K
- **LogiFlow** — LogTech Last-mile SaaS — Series A — México — ARR $3.2M
- **MediSync** — HealthTech SaaS clínico — Pre-Seed — Colombia — ARR $36K (Studio)
- **CreditIA** — Fintech Digital Lending — Seed — Colombia — ARR $620K (Studio)
- **AgriSense** — AgriTech Precision farming — Seed — Colombia — ARR $390K

### data/studio_seed_data.py — Venture Studio (95 registros)
- **EduStack** — EdTech SaaS B2B — fase MVP
- **LegalBot** — LegalTech AI — fase Validación
- **FleetOS** — LogTech flotillas — fase Seed externo (empresa más madura)
- **InsureX** — InsurTech embedded — fase Idea
- **TaxFlow** — Fintech contabilidad PYME — fase Validación

---

## Contexto de negocio

- **Fondo:** AIDA Ventures Fund I — tamaño parametrizable (default demo $10M)
- **Etapas:** Pre-Seed / Seed / Series A
- **Geografía:** Colombia (foco) + LATAM
- **Sectores core:** Fintech, SaaS, LogTech
- **Venture Studio:** Activo — el sistema mide alpha studio vs mercado
- **Startups reales:** 0 — todo simulado para desarrollo
- **Modo actual:** Demo — datos 100% ficticios

---

## Endpoints disponibles en la API

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Bienvenida |
| GET | `/health` | Estado del servidor |
| GET | `/startups` | Lista con filtros: sector, stage, country, studio_built |
| GET | `/startups/{id}` | Detalle de startup |
| GET | `/startups/{id}/metrics` | Métricas históricas |
| GET | `/startups/{id}/metrics/latest` | Último snapshot por métrica |
| GET | `/startups/{id}/percentile` | Posición percentil vs benchmark |
| GET | `/market/segments` | Segmentos de mercado con filtros |
| GET | `/market/benchmarks` | Benchmarks P25/P50/P75/P90 |

---

## Progreso del desarrollo

### Fase 0 — Fundaciones ✅ COMPLETA
- [x] Entorno Python configurado (venv, dependencias)
- [x] PostgreSQL local con DB `aida_venture_os`
- [x] Repositorio GitHub configurado
- [x] Estructura de carpetas completa
- [x] `app/database.py` — conexión SQLAlchemy
- [x] `app/main.py` — FastAPI con / y /health operativos
- [x] 9 archivos de modelos SQLAlchemy — 43 tablas
- [x] `alembic.ini` + configuración de migraciones
- [x] Primera migración y creación de tablas en DB
- [x] `data/load_seed.py` — 255 registros simulados iniciales

### Fase 1 — Motor de comparabilidad ✅ COMPLETA
- [x] `app/schemas/startup.py` y `app/schemas/market.py` — Pydantic v2
- [x] `app/routers/startups.py` — 5 endpoints operativos
- [x] `app/routers/market.py` — 2 endpoints con filtros
- [x] `app/services/percentile.py` — cálculo percentil con interpolación lineal
- [x] `data/load_benchmarks.py` — 54 segmentos + 119 benchmarks desde Excels
- [x] `data/load_seed_extended.py` — currencies, tags, fintech_subverticals, sourcing_channels, deals, ic_memos, valuation_events
- [x] 503 registros totales en DB

### Fase 2 — Simulador y Studio ← ESTAMOS AQUÍ
- [ ] Valuation Intelligence — router + cálculo múltiplos vs mercado
- [ ] Fund Simulator — Monte Carlo MOIC/IRR parametrizable
- [ ] Studio Performance — router + endpoints alpha
- [ ] Fintech Deep Dive — unit economics y comparables por subvertical
- [ ] Deal Flow — router + endpoints para pipeline
- [ ] Reporting básico — lp_profiles + reports

### Fase 3 — Demo completo
- [ ] Deal Flow & Sourcing completo
- [ ] Reporting para LPs
- [ ] Sistema de roles (gp / analyst / studio_operator / viewer)
- [ ] Formulario de ingesta de métricas para startups
- [ ] Tests por dominio

---

## Comandos frecuentes

```bash
# Activar entorno virtual
.\venv\Scripts\activate

# Iniciar servidor (mantener corriendo en terminal separada)
uvicorn app.main:app --reload

# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

---

## Instrucciones para Claude Code

1. **Siempre leer este archivo** al inicio de cada sesión antes de escribir código
2. **Actualizar el estado** de las tareas (⬜ → 🔄 → ✅) cuando se completen
3. **Seguir las convenciones** de código definidas arriba sin excepción
4. **No crear archivos fuera** de la estructura definida sin consultarlo
5. **Cada modelo nuevo** debe importar `Base` desde `app.database`
6. **Cada router nuevo** debe registrarse en `app/main.py`
7. **Pedir confirmación** antes de modificar archivos que ya están marcados como ✅