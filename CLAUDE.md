# CLAUDE.md — Memoria del proyecto AIDA Venture OS

Este archivo es leído automáticamente por Claude Code en cada sesión.
Contiene todo el contexto necesario para continuar el desarrollo sin repetir instrucciones.

---

## Identidad del proyecto

**Nombre:** AIDA Venture OS  
**Descripción:** Sistema operativo de decisión para venture capital y venture studio.  
**Empresa:** AIDA Ventures + Scale Radical  
**Estado actual:** Demo funcional con datos 100% simulados  
**Objetivo inmediato:** Backend funcional con APIs, modelos de DB y seed data cargado  

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
│   ├── main.py              ✅ CREADO — FastAPI entry point
│   ├── database.py          ✅ CREADO — conexión PostgreSQL con SQLAlchemy
│   ├── models/
│   │   ├── __init__.py      ✅ CREADO
│   │   ├── shared.py        ✅ CREADO — users, currencies, tags, audit_logs
│   │   ├── startup.py       🔄 EN PROGRESO — startups, founders, metric_snapshots
│   │   ├── valuation.py     ⬜ PENDIENTE
│   │   ├── fund.py          ⬜ PENDIENTE
│   │   ├── studio.py        ⬜ PENDIENTE
│   │   ├── fintech.py       ⬜ PENDIENTE
│   │   ├── dealflow.py      ⬜ PENDIENTE
│   │   └── reporting.py     ⬜ PENDIENTE
│   ├── schemas/             ⬜ PENDIENTE — Pydantic v2 schemas
│   ├── routers/             ⬜ PENDIENTE — endpoints REST
│   └── services/            ⬜ PENDIENTE — lógica de negocio
├── alembic/                 ✅ CREADO — carpeta con .gitkeep
├── data/
│   ├── seed_data.py         ✅ CREADO — 5 startups portafolio simuladas
│   ├── studio_seed_data.py  ✅ CREADO — 5 empresas studio simuladas
│   └── *.xlsx               ✅ CARGADOS — benchmarks externos
├── tests/                   ✅ CREADO — carpeta con __init__.py
├── .env                     ✅ CREADO — credenciales locales (no en GitHub)
├── .env.example             ✅ CREADO — template público
├── requirements.txt         ✅ CREADO
├── README.md                ✅ CREADO
└── CLAUDE.md                ✅ ESTE ARCHIVO
```

---

## Base de datos

**Nombre:** `aida_venture_os`  
**Usuario:** `postgres`  
**Puerto:** `5432`  
**Host:** `localhost`  
**Connection string:** en `.env` como `DATABASE_URL`

### 43 tablas en 8 dominios

| Dominio | Tablas | Estado |
|---|---|---|
| Transversales | users, currencies, tags, audit_logs | ✅ Modelos creados |
| Startup Engine | startups, founders, startup_founders, funding_rounds, metric_snapshots, cohort_analyses | 🔄 En progreso |
| Market Reality | market_segments, benchmark_entries, benchmark_series, valuation_distributions | ⬜ Pendiente |
| Valuation Intel | valuation_events, multiple_analyses, valuation_drivers, outlier_flags | ⬜ Pendiente |
| Fund Simulator | funds, lps, investments, portfolio_allocations, deal_assumptions, fund_scenarios, fund_metrics | ⬜ Pendiente |
| Studio Performance | studio_companies, build_costs, studio_milestones, alpha_metrics | ⬜ Pendiente |
| Fintech Deep Dive | fintech_subverticals, fintech_unit_economics, regulatory_risks, fintech_comparables | ⬜ Pendiente |
| Deal Flow | deal_opportunities, thesis_alignments, sourcing_channels, dd_checklists, ic_memos | ⬜ Pendiente |
| Reporting | lp_profiles, reports, narrative_blocks, ic_decisions | ⬜ Pendiente |

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

## Progreso del desarrollo

### Fase 0 — Fundaciones ← COMPLETA ✅
- [x] Entorno Python configurado (venv, dependencias)
- [x] PostgreSQL local con DB `aida_venture_os`
- [x] Repositorio GitHub configurado
- [x] Estructura de carpetas completa
- [x] `app/database.py` — conexión SQLAlchemy
- [x] `app/main.py` — FastAPI con / y /health operativos
- [x] `app/models/shared.py` — 4 tablas transversales
- [x] `app/models/startup.py` — en progreso
- [x] Modelos restantes (6 archivos)
- [x] `alembic.ini` + configuración de migraciones
- [x] Primera migración y creación de tablas en DB
- [x] Carga de seed data

### Fase 1 — Motor de comparabilidad
- [ ] APIs Market Reality + Startup Engine
- [ ] Servicio de cálculo de percentiles
- [ ] Importador de Excels

### Fase 2 — Simulador y Studio
- [ ] Valuation Intelligence
- [ ] Fund Simulator con Monte Carlo
- [ ] Studio Performance + alpha metrics

### Fase 3 — Demo completo
- [ ] Deal Flow & Sourcing
- [ ] Reporting para LPs
- [ ] Sistema de roles
- [ ] Formulario de ingesta de métricas

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