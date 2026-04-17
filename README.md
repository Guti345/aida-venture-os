# AIDA Venture OS

> Sistema operativo de decisión para venture capital y venture studio — AIDA Ventures + Scale Radical

---

## ¿Qué es este sistema?

Este no es un dashboard. Es el **sistema nervioso central del fondo** — una plataforma de inteligencia que convierte datos dispersos en decisiones comparables, auditables y reproducibles.

Responde tres preguntas fundamentales en todo momento:

| Pregunta | Dominio | Output |
|---|---|---|
| **¿Dónde invertir?** | Market Reality + Deal Flow + Fintech | Benchmarks por segmento, gaps de mercado, scoring de deals |
| **¿Cuánto vale?** | Valuation Intel + Startup Engine | Múltiplos de entrada vs mercado, percentil por métrica |
| **¿Cómo optimizamos retornos?** | Fund Simulator + Studio Performance | Escenarios MOIC/IRR, alpha del studio, alertas de portafolio |

---

## Estado actual del proyecto

> **Fase 1 completada — Fase 2 en curso**
> Backend operativo con 43 tablas en PostgreSQL y 503 registros simulados cargados.
> Motor de comparabilidad operativo con percentiles reales. Construyendo Valuation Intel y Fund Simulator.

### Decisiones de arquitectura confirmadas

| Pregunta | Decisión |
|---|---|
| ¿Startups en portafolio real? | No. Se usan 5 startups simuladas + 5 del venture studio simulado |
| ¿Tamaño del fondo? | Parámetro ajustable en la UI — sin valor fijo |
| ¿Frecuencia de reporte? | Por definir. Sistema preparado para ingesta via formulario o Excel |
| ¿Multi-tenant o single-tenant? | Single-tenant — uso exclusivo de AIDA Ventures |
| ¿Usuarios del sistema? | GPs, analistas del fondo, operadores del venture studio |
| ¿Objetivo inmediato? | Demo funcional para recolección de datos, BI y reportes para LPs |

---

## Datos simulados — fase de desarrollo

El sistema opera con **255 registros simulados** en base de datos:

### Portafolio externo (5 startups)

| Startup | Sector | Etapa | ARR simulado | País |
|---|---|---|---|---|
| FinStack | Fintech / Neobank B2B | Seed | $480K | Colombia |
| LogiFlow | LogTech / Last-mile SaaS | Series A | $3.2M | México |
| MediSync | HealthTech / SaaS clínico | Pre-Seed | $36K | Colombia |
| CreditIA | Fintech / Digital Lending | Seed | $620K | Colombia |
| AgriSense | AgriTech / Precision farming | Seed | $390K | Colombia |

### Venture studio (5 empresas simuladas)

| Empresa | Sector | Fase studio | Estado |
|---|---|---|---|
| EduStack | EdTech / SaaS B2B | MVP | En construcción |
| LegalBot | LegalTech / AI | Validación | En construcción |
| FleetOS | LogTech / Gestión flotillas | Seed externo | Empresa de referencia del studio |
| InsureX | InsurTech / Embedded | Idea | En construcción |
| TaxFlow | Fintech / Contabilidad PYME | Validación | En construcción |

> **Nota:** Todos estos datos son ficticios y serán reemplazados con información real
> cuando el fondo y el studio comiencen operaciones con startups reales.

### Registros en base de datos

| Tabla | Registros |
|---|---|
| currencies | 5 |
| tags | 14 |
| startups | 10 |
| founders | 20 |
| startup_founders | 20 |
| funding_rounds | 9 |
| metric_snapshots | 138 |
| market_segments | 54 |
| benchmark_entries | 119 |
| valuation_events | 9 |
| funds | 1 |
| investments | 9 |
| studio_companies | 7 |
| build_costs | 16 |
| studio_milestones | 19 |
| alpha_metrics | 6 |
| fintech_subverticals | 6 |
| sourcing_channels | 6 |
| deal_opportunities | 8 |
| thesis_alignments | 10 |
| dd_checklists | 14 |
| ic_memos | 3 |
| **Total** | **503** |

### Plan de transición datos simulados → datos reales

```
Fase demo (hoy)     → Datos inventados en seed_data.py y studio_seed_data.py
Fase piloto         → GP ingresa datos manualmente via formulario en el sistema
Fase operacional    → Startups reportan via formulario mensual (Google Form o UI propia)
Fase automatizada   → Integración directa con fuentes (contabilidad, CRM, bancos)
```

---

## Roles y perfiles de usuario

| Perfil | Acceso | Capacidades |
|---|---|---|
| `gp` | Total | Todas las vistas, simulador del fondo, configuración |
| `analyst` | Lectura + entrada de datos | Startups, métricas, deals, reportes — sin simulador ni config del fondo |
| `studio_operator` | Studio + startups propias | Solo empresas del venture studio y sus métricas |
| `viewer` | Solo lectura | Dashboards y reportes — sin edición. Para LPs con acceso limitado |

---

## Stack tecnológico

| Componente | Tecnología | Versión |
|---|---|---|
| Lenguaje | Python | 3.14 |
| Framework API | FastAPI + Uvicorn | Latest |
| Base de datos | PostgreSQL | 18 (local, puerto 5432) |
| ORM | SQLAlchemy + Alembic | Latest |
| Validación | Pydantic | v2 |
| Procesamiento | Pandas + NumPy + SciPy | Latest |
| Entorno | virtualenv (venv) | — |
| Control de versiones | Git + GitHub Desktop | — |

---

## Estructura del proyecto

```
aida-venture-os/
│
├── app/
│   ├── main.py                  ✅ FastAPI entry point — / y /health operativos
│   ├── database.py              ✅ Conexión PostgreSQL con SQLAlchemy
│   │
│   ├── models/                  ✅ 43 tablas en 8 dominios — COMPLETO
│   │   ├── __init__.py          ✅ Importaciones ordenadas por grafo FK
│   │   ├── shared.py            ✅ users, currencies, tags, audit_logs
│   │   ├── market.py            ✅ market_segments, benchmark_entries, benchmark_series, valuation_distributions
│   │   ├── startup.py           ✅ startups, founders, startup_founders, funding_rounds, metric_snapshots
│   │   ├── valuation.py         ✅ valuation_events, multiple_analyses, valuation_drivers, outlier_flags
│   │   ├── fund.py              ✅ funds, lps, investments, fund_scenarios, fund_metrics
│   │   ├── studio.py            ✅ studio_companies, build_costs, studio_milestones, alpha_metrics
│   │   ├── fintech.py           ✅ fintech_subverticals, fintech_unit_economics, regulatory_risks, fintech_comparables
│   │   ├── dealflow.py          ✅ deal_opportunities, thesis_alignments, sourcing_channels, dd_checklists, ic_memos
│   │   └── reporting.py         ✅ lp_profiles, reports, narrative_blocks, ic_decisions
│   │
│   ├── schemas/                 ✅ Pydantic v2 schemas — startup.py + market.py
│   │   ├── startup.py           ✅ StartupList, StartupRead, StartupWithMetrics, MetricSnapshotRead
│   │   └── market.py            ✅ MarketSegmentRead, BenchmarkEntryRead, PercentileResult
│   ├── routers/                 ✅ Endpoints REST operativos — 2 routers activos
│   │   ├── startups.py          ✅ 5 endpoints — lista, detalle, métricas, percentil, métricas latest
│   │   └── market.py            ✅ 2 endpoints — segmentos y benchmarks con filtros
│   └── services/                🔄 En construcción — lógica de negocio
│       ├── percentile.py        ✅ Cálculo de percentiles vs benchmarks con interpolación lineal
│       ├── simulator.py         ⬜ Monte Carlo MOIC/IRR
│       ├── alpha.py             ⬜ Studio alpha vs mercado
│       └── importer.py          ⬜ Importación de Excels a DB
│
├── alembic/                     ✅ Migraciones configuradas
│   ├── env.py                   ✅ Conectado a .env y Base
│   ├── script.py.mako           ✅
│   └── versions/
│       └── 8261c3862e5b_*.py    ✅ Migración inicial — 43 tablas creadas
│
├── data/                        ✅ Datos semilla cargados en DB
│   ├── seed_data.py             ✅ 5 startups portafolio + fondo (147 registros)
│   ├── studio_seed_data.py      ✅ 5 empresas venture studio (95 registros)
│   ├── load_seed.py             ✅ Cargador unificado idempotente — 255 registros insertados
│   ├── load_benchmarks.py       ✅ Benchmarks desde Excels — 54 segmentos + 119 benchmarks
│   ├── load_seed_extended.py    ✅ Seed extendida Fase 2 — 75 registros adicionales
│   ├── VCFunds_Metrics.xlsx     ✅
│   ├── Venture_Studio_Metrics_Reference.xlsx ✅
│   ├── _AIDA_Ventures_-_Startups_Benchmarks.xlsx ✅
│   ├── _Metricas_Startups.xlsx  ✅
│   └── Fintech_Sectors.xlsx     ✅
│
├── tests/                       ⬜ Pendiente
├── .env                         ✅ Configurado — NO subir a GitHub
├── .env.example                 ✅
├── requirements.txt             ✅
├── alembic.ini                  ✅
├── CLAUDE.md                    ✅ Memoria persistente para Claude Code
└── README.md                    ✅ Este archivo
```

---

## Base de datos — 43 tablas en 8 dominios

| Dominio | Tablas | Modelo | Migración | Seed data |
|---|---|---|---|---|
| Transversales | users, currencies, tags, audit_logs | ✅ | ✅ | ⬜ |
| Startup Engine | startups, founders, startup_founders, funding_rounds, metric_snapshots | ✅ | ✅ | ✅ |
| Market Reality | market_segments, benchmark_entries, benchmark_series, valuation_distributions | ✅ | ✅ | ⬜ |
| Valuation Intel | valuation_events, multiple_analyses, valuation_drivers, outlier_flags | ✅ | ✅ | ⬜ |
| Fund Simulator | funds, lps, investments, fund_scenarios, fund_metrics | ✅ | ✅ | ✅ |
| Studio Performance | studio_companies, build_costs, studio_milestones, alpha_metrics | ✅ | ✅ | ✅ |
| Fintech Deep Dive | fintech_subverticals, fintech_unit_economics, regulatory_risks, fintech_comparables | ✅ | ✅ | ⬜ |
| Deal Flow | deal_opportunities, thesis_alignments, sourcing_channels, dd_checklists, ic_memos | ✅ | ✅ | ⬜ |
| Reporting | lp_profiles, reports, narrative_blocks, ic_decisions | ✅ | ✅ | ⬜ |

---

## Variables de entorno

```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/aida_venture_os
SECRET_KEY=genera-una-clave-larga-y-aleatoria
ENVIRONMENT=development
DEBUG=True
FUND_TARGET_SIZE_USD=10000000
```

El archivo `.env` está en `.gitignore` — nunca se sube a GitHub.

---

## Cómo correr el proyecto

```bash
# 1. Activar entorno virtual
.\venv\Scripts\activate

# 2. Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# 3. Crear tablas en PostgreSQL
alembic upgrade head

# 4. Cargar datos simulados
python data/load_seed.py

# 5. Iniciar el servidor
uvicorn app.main:app --reload
```

Disponible en:
- `http://localhost:8000` — API
- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — ReDoc

---

## Plan de desarrollo por fases

### Fase 0 — Fundaciones ✅ COMPLETA
- [x] Entorno Python configurado (venv, dependencias)
- [x] PostgreSQL local con DB `aida_venture_os`
- [x] Repositorio GitHub configurado
- [x] Estructura de carpetas completa
- [x] `app/database.py` — conexión SQLAlchemy
- [x] `app/main.py` — FastAPI con / y /health operativos
- [x] 9 archivos de modelos SQLAlchemy — 43 tablas
- [x] `alembic.ini` + `env.py` configurados
- [x] Migración inicial — 43 tablas creadas en PostgreSQL
- [x] `data/load_seed.py` — 255 registros simulados cargados
- [x] `CLAUDE.md` — memoria persistente para Claude Code

### Fase 1 — Motor de comparabilidad ✅ COMPLETA
- [x] Schemas Pydantic — `app/schemas/startup.py` y `app/schemas/market.py`
- [x] Router startups — `app/routers/startups.py` con CRUD y métricas
- [x] Router market — `app/routers/market.py` con benchmarks y segmentos
- [x] Servicio `app/services/percentile.py` — startup X en percentil Y vs benchmark
- [x] Importador de Excels — cargar benchmarks desde los 5 archivos .xlsx
- [x] Benchmarks seed cargados en `market_segments` y `benchmark_entries`
- [x] Registrar routers en `app/main.py`
- [x] Seed extendida — `data/load_seed_extended.py` — currencies, tags, fintech_subverticals, sourcing_channels, deals, ic_memos, valuation_events

### Fase 2 — Simulador y studio ← ESTAMOS AQUÍ
- [ ] Valuation Intelligence — schemas + router + cálculo de múltiplos vs mercado
- [ ] Fund Simulator — Monte Carlo MOIC/IRR con fondo parametrizable
- [ ] Studio Performance — alpha vs mercado (router + endpoints)
- [ ] Fintech Deep Dive — unit economics y comparables por subvertical
- [ ] Deal Flow — router + endpoints para pipeline de deals
- [ ] LPs y reporting básico

### Fase 3 — Demo completo (semanas 9–10)
- [ ] Deal Flow & Sourcing — pipeline completo
- [ ] Reporting — generador de LP reports
- [ ] Sistema de roles (gp / analyst / studio_operator / viewer)
- [ ] Formulario de ingesta de métricas para startups
- [ ] Tests por dominio

### Fase 4 — Transición a datos reales (post-demo)
- [ ] Reemplazar seed data por datos reales del fondo
- [ ] Proceso de reporte periódico con startups reales
- [ ] Onboarding de primeros LPs como viewers

---

## Endpoints disponibles en la API

### Sistema
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Health check básico |
| GET | `/health` | Estado del servidor |

### Startups (`/startups`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/startups` | Lista todas las startups — filtros: sector, stage, country, studio_built |
| GET | `/startups/{id}` | Detalle de una startup |
| GET | `/startups/{id}/metrics` | Métricas históricas — filtro: metric_name |
| GET | `/startups/{id}/metrics/latest` | Último snapshot por cada métrica |
| GET | `/startups/{id}/percentile` | Posición percentil vs benchmark — params: metric_name, segment_id |

### Market (`/market`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/market/segments` | Segmentos de mercado — filtros: sector, stage, geography, country |
| GET | `/market/benchmarks` | Benchmarks P25/P50/P75/P90 — filtros: segment_id, multiple_type, sector |

---

## Reglas de desarrollo

1. **No promedios — siempre percentiles.** Toda comparación usa P25/P50/P75/P90.
2. **Toda métrica tiene fecha y fuente.** Sin `period_date` y `source` no se guarda.
3. **Módulos independientes.** Cada dominio vive en su propio archivo.
4. **Nunca credenciales en el código.** Siempre `.env` + `python-dotenv`.
5. **Cada endpoint tiene su schema Pydantic.** Sin validación no hay endpoint.
6. **Commits atómicos.** Un commit = una funcionalidad completa.
7. **El tamaño del fondo es siempre un parámetro.** Nunca hardcodeado.
8. **Los datos simulados se marcan explícitamente.** Campo `is_simulated: bool` en startups.

---

## Contexto de negocio

| Parámetro | Valor |
|---|---|
| Fondo | AIDA Ventures + Scale Radical |
| Etapas objetivo | Pre-Seed / Seed / Series A |
| Geografía foco | Colombia, LATAM |
| Sectores core | Fintech, SaaS, LogTech |
| Venture Studio | Activo — el sistema mide alpha vs mercado |
| Tamaño del fondo | Parámetro ajustable (default demo: $10M) |
| Startups en portafolio real | 0 — sistema en modo demo con datos simulados |
| Empresas studio reales | 0 — sistema en modo demo con datos simulados |
| Usuarios del sistema | GPs y analistas internos + operadores del studio |
| Objetivo inmediato | Demo funcional para BI y reportes LP |

---

*Última actualización: Abril 2026 — AIDA Ventures*
*Estado: Fase 1 completa — Fase 2 en curso*
*Base de datos: 43 tablas creadas — 503 registros simulados cargados*