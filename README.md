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

> **Fase 4 completa — frontend Next.js operativo**
> Backend con 43 tablas en PostgreSQL, 503 registros simulados, 57 rutas REST, autenticación JWT con roles y 10 tests de integración.
> Frontend Next.js con 7 secciones operativas, mock data con fallback a API real.
> **Objetivo inmediato:** CI/CD (GitHub Actions), seed data extendida para reporting, autenticación real en UI.

### Decisiones de arquitectura confirmadas

| Pregunta | Decisión |
|---|---|
| ¿Startups en portafolio real? | No. Se usan 5 startups simuladas + 5 del venture studio simulado |
| ¿Tamaño del fondo? | Parámetro ajustable en la UI — sin valor fijo |
| ¿Frecuencia de reporte? | Por definir. Sistema preparado para ingesta via formulario o Excel |
| ¿Multi-tenant o single-tenant? | Single-tenant — uso exclusivo de AIDA Ventures |
| ¿Usuarios del sistema? | GPs, analistas del fondo, operadores del venture studio |
| ¿Objetivo inmediato? | CI/CD, seed data extendida para reporting, autenticación real en UI |

---

## Datos simulados — fase de desarrollo

El sistema opera con **503 registros simulados** en base de datos:

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

| Dominio | Tablas | Registros |
|---|---|---|
| Transversales | users, currencies, tags, audit_logs | 19 |
| Startup Engine | startups, founders, startup_founders, funding_rounds, metric_snapshots | 197 |
| Market Reality | market_segments, benchmark_entries, benchmark_series, valuation_distributions | 173 |
| Valuation Intel | valuation_events, multiple_analyses, valuation_drivers, outlier_flags | 9 |
| Fund Simulator | funds, lps, investments, fund_scenarios, fund_metrics | 10 |
| Studio Performance | studio_companies, build_costs, studio_milestones, alpha_metrics | 48 |
| Fintech Deep Dive | fintech_subverticals, fintech_unit_economics, regulatory_risks, fintech_comparables | 6 |
| Deal Flow | deal_opportunities, thesis_alignments, sourcing_channels, dd_checklists, ic_memos | 41 |
| Reporting | lp_profiles, reports, narrative_blocks, ic_decisions | 0 |
| **Total** | | **503** |

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
| Frontend | Next.js 14 + React 18 + Tailwind CSS v3 | — |
| Charts | Recharts | — |
| Control de versiones | Git + GitHub | — |

---

## Estructura del proyecto

```
aida-venture-os/
├── app/
│   ├── main.py              ✅ FastAPI entry point — 9 routers, 57 rutas totales
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
│   │   ├── auth.py          ✅ UserCreate, UserRead, Token, LoginRequest
│   │   ├── startup.py       ✅ StartupList, StartupRead, StartupWithMetrics, MetricSnapshotRead, MetricIngestionForm
│   │   ├── market.py        ✅ MarketSegmentRead, BenchmarkEntryRead, PercentileResult
│   │   ├── valuation.py     ✅ ValuationEventRead, MultipleAnalysisRead, ValuationAnalysisResult
│   │   ├── fund.py          ✅ FundRead, InvestmentRead, FundMetricsRead, ScenarioInput, ScenarioResult
│   │   ├── studio.py        ✅ StudioCompanyRead, BuildCostRead, StudioSummary, TimelineEvent
│   │   ├── fintech.py       ✅ FintechSubverticalRead, FintechMarketOverview, RegulatoryRiskRead
│   │   ├── dealflow.py      ✅ DealOpportunityRead, ThesisAlignmentRead, DDChecklistRead, ICMemoRead
│   │   └── reporting.py     ✅ LPProfileRead, ReportRead, LPReportSummary, PortfolioSnapshotItem
│   ├── routers/
│   │   ├── auth.py          ✅ 6 endpoints — register, login, me, users, deactivate
│   │   ├── startups.py      ✅ 6 endpoints — lista, detalle, métricas, percentil, latest, ingest-metrics
│   │   ├── market.py        ✅ 2 endpoints — segmentos y benchmarks con filtros
│   │   ├── valuation.py     ✅ 5 endpoints — events, event detail, analyze, drivers, outliers
│   │   ├── fund.py          ✅ 6 endpoints — fondo, inversiones, metrics, scenarios, simulate, quick
│   │   ├── studio.py        ✅ 8 endpoints — summary, companies, detail, timeline, costs, milestones, alpha
│   │   ├── fintech.py       ✅ 6 endpoints — subverticals, overview, unit-economics, comparables, regulatory-risks
│   │   ├── dealflow.py      ✅ 8 endpoints — deals + sourcing channels
│   │   └── reporting.py     ✅ 4 endpoints — lp-summary, portfolio-snapshot, ic-decisions, pipeline-status
│   └── services/
│       ├── auth.py          ✅ JWT, hash_password, roles (gp/analyst/studio_operator/viewer)
│       ├── percentile.py    ✅ Cálculo de percentiles con interpolación lineal
│       ├── valuation.py     ✅ analyze_valuation — múltiplo vs benchmark, verdict, premium_pct
│       ├── simulator.py     ✅ run_monte_carlo — N iteraciones vectorizadas con numpy
│       ├── alpha.py         ✅ get_studio_summary, get_company_timeline, calculate_alpha_score
│       └── importer.py      ✅ ingest_metrics — upsert por startup+métrica+período, warnings automáticos
├── alembic/                 ✅ Migraciones configuradas — 43 tablas en producción
├── data/
│   ├── seed_data.py         ✅ 5 startups portafolio + fondo (147 registros)
│   ├── studio_seed_data.py  ✅ 5 empresas venture studio (95 registros)
│   ├── load_seed.py         ✅ Cargador unificado idempotente — 255 registros
│   ├── load_benchmarks.py   ✅ Benchmarks desde Excels — 54 segmentos + 119 benchmarks
│   ├── load_seed_extended.py ✅ Seed extendida — 75 registros adicionales
│   ├── create_admin.py      ✅ Bootstrap GP: admin@aidaventures.co / AidaVC2025!
│   └── *.xlsx               ✅ 5 archivos de benchmarks externos
├── tests/
│   ├── conftest.py          ✅ TestClient + auth_headers fixtures
│   ├── test_startups.py     ✅ 5 tests — list, by name, ARR latest, percentile, ingest-metrics
│   ├── test_fund.py         ✅ 3 tests — fund exists, quick simulate MOIC, scenarios
│   └── test_reports.py      ✅ 2 tests — lp-summary fields, portfolio snapshot
├── frontend/
│   ├── app/
│   │   ├── layout.tsx              ✅ Root layout — sidebar + topbar
│   │   ├── page.tsx                ✅ Dashboard — 4 KPIs, tabla portafolio, studio donut, deals bar
│   │   ├── portfolio/page.tsx      ✅ Lista startups con filtros (sector, stage, país, nombre)
│   │   ├── portfolio/[name]/       ✅ Detalle startup — ARR histórico, percentil vs mercado
│   │   ├── fund/page.tsx           ✅ Simulador Monte Carlo — sliders, P25/P50/P75 MOIC+IRR
│   │   ├── studio/page.tsx         ✅ Venture Studio — donut por fase, alpha metrics
│   │   ├── deals/page.tsx          ✅ Pipeline — tabla con thesis scores, canales sourcing
│   │   ├── market/page.tsx         ✅ Benchmarks por segmento — bar chart + tabla
│   │   └── reports/page.tsx        ✅ LP Report — resumen narrativo + portfolio snapshot
│   ├── components/
│   │   ├── layout/                 ✅ Sidebar (navy, colapsable), Topbar, PageWrapper
│   │   ├── ui/                     ✅ Card, KPICard, Badge, Table, SectionTitle, EmptyState
│   │   └── charts/                 ✅ BarChart, LineChart, DonutChart (Recharts wrappers)
│   └── lib/
│       ├── api.ts                  ✅ Cliente HTTP — intenta API real, fallback a mock
│       ├── types.ts                ✅ Interfaces TypeScript alineadas con backend schemas
│       └── mock/                   ✅ portfolio.ts, fund.ts, studio.ts, deals.ts, reports.ts
├── .env                     ✅ Credenciales locales — NO subir a GitHub
├── .env.example             ✅ Template público
├── requirements.txt         ✅
├── CLAUDE.md                ✅ Memoria persistente para Claude Code
└── README.md                ✅ Este archivo
```

---

## Base de datos — 43 tablas en 8 dominios

| Dominio | Tablas | Modelo | Seed data | Registros |
|---|---|---|---|---|
| Transversales | users, currencies, tags, audit_logs | ✅ | 🔄 parcial | 19 |
| Startup Engine | startups, founders, startup_founders, funding_rounds, metric_snapshots | ✅ | ✅ | 197 |
| Market Reality | market_segments, benchmark_entries, benchmark_series, valuation_distributions | ✅ | ✅ | 173 |
| Valuation Intel | valuation_events, multiple_analyses, valuation_drivers, outlier_flags | ✅ | 🔄 parcial | 9 |
| Fund Simulator | funds, lps, investments, fund_scenarios, fund_metrics | ✅ | 🔄 parcial | 10 |
| Studio Performance | studio_companies, build_costs, studio_milestones, alpha_metrics | ✅ | ✅ | 48 |
| Fintech Deep Dive | fintech_subverticals, fintech_unit_economics, regulatory_risks, fintech_comparables | ✅ | 🔄 parcial | 6 |
| Deal Flow | deal_opportunities, thesis_alignments, sourcing_channels, dd_checklists, ic_memos | ✅ | ✅ | 41 |
| Reporting | lp_profiles, reports, narrative_blocks, ic_decisions | ✅ | ⬜ | 0 |

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

### Backend

```bash
# 1. Activar entorno virtual
.\venv\Scripts\activate

# 2. Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# 3. Crear tablas en PostgreSQL
alembic upgrade head

# 4. Cargar datos simulados
python data/load_seed.py
python data/load_benchmarks.py
python data/load_seed_extended.py

# 5. Crear usuario administrador
python data/create_admin.py

# 6. Iniciar el servidor
uvicorn app.main:app --reload
```

Backend disponible en:
- `http://localhost:8000` — API REST
- `http://localhost:8000/docs` — Swagger UI interactivo
- `http://localhost:8000/redoc` — ReDoc

### Frontend

```bash
cd frontend
npm install       # solo la primera vez
npm run dev       # abre http://localhost:3000
```

Crea `frontend/.env.local` para conectar contra la API local:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEMO_TOKEN=<tu_jwt_token>
```

Sin estas variables el frontend usa **mock data** como fallback automático.

### Tests

```bash
pytest tests/ -v   # 10 tests de integración
```

---

## Plan de desarrollo por fases

### Fase 0 — Fundaciones ✅ COMPLETA
- [x] Entorno Python configurado (venv, dependencias)
- [x] PostgreSQL local con DB `aida_venture_os`
- [x] Repositorio GitHub configurado
- [x] 9 archivos de modelos SQLAlchemy — 43 tablas
- [x] Alembic configurado — migración inicial aplicada
- [x] `data/load_seed.py` — 255 registros simulados cargados

### Fase 1 — Motor de comparabilidad ✅ COMPLETA
- [x] Schemas Pydantic — `startup.py` y `market.py`
- [x] Router startups — lista, detalle, métricas, percentil, latest
- [x] Router market — benchmarks y segmentos con filtros
- [x] `services/percentile.py` — cálculo percentil con interpolación lineal
- [x] `data/load_benchmarks.py` — 54 segmentos + 119 benchmarks desde Excels
- [x] `data/load_seed_extended.py` — currencies, tags, fintech_subverticals, sourcing_channels, deals, ic_memos, valuation_events

### Fase 2 — Simulador y Studio ✅ COMPLETA
- [x] Valuation Intelligence — schemas + service analyze_valuation + router 5 endpoints
- [x] Fund Simulator — Monte Carlo MOIC/IRR vectorizado con numpy, 6 endpoints
- [x] Studio Performance — summary, timeline, alpha score, 8 endpoints
- [x] Fintech Deep Dive — unit economics, comparables, regulatory-risks, 6 endpoints
- [x] Deal Flow & Sourcing — pipeline con thesis scoring, DD progress, IC memos, 8 endpoints
- [x] Reporting básico — lp-summary, portfolio snapshot, ic-decisions, pipeline-status, 4 endpoints

### Fase 3 — Demo completo ✅ COMPLETA
- [x] Sistema de autenticación JWT con roles (gp / analyst / studio_operator / viewer)
- [x] Bootstrap: `data/create_admin.py` — `admin@aidaventures.co` / `AidaVC2025!`
- [x] Formulario de ingesta de métricas — `POST /startups/ingest-metrics` (require_analyst)
- [x] Tests de integración — 10 tests pasando (`pytest tests/ -v`)

### Fase 4 — Frontend ✅ COMPLETA
- [x] Next.js 14 con 7 secciones operativas
- [x] Mock data con fallback automático a API real
- [x] Sidebar colapsable, paleta institucional, Recharts

### Próximos pasos
- [ ] CI/CD (GitHub Actions)
- [ ] Seed data extendida para dominio Reporting
- [ ] Autenticación real en UI (login screen + JWT persistido)

---

## Endpoints disponibles en la API

### Sistema
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Bienvenida |
| GET | `/health` | Estado del servidor |

### Auth (`/auth`)
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/auth/register` | Bootstrap primer usuario (solo si DB vacía) |
| POST | `/auth/register/admin` | Registrar usuario — require_gp |
| POST | `/auth/login` | Login → JWT token |
| GET | `/auth/me` | Usuario autenticado actual |
| GET | `/auth/users` | Lista usuarios — require_gp |
| PUT | `/auth/users/{user_id}/deactivate` | Desactivar usuario — require_gp |

### Startups (`/startups`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/startups` | Lista con filtros: name, sector, stage, country, studio_built |
| GET | `/startups/{id}` | Detalle de startup por UUID |
| GET | `/startups/{name}/metrics` | Métricas históricas por nombre |
| GET | `/startups/{name}/metrics/latest` | Último snapshot por métrica |
| GET | `/startups/{name}/percentile` | Percentil vs benchmark |
| POST | `/startups/ingest-metrics` | Ingesta mensual — require_analyst |

### Market (`/market`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/market/segments` | Segmentos de mercado con filtros |
| GET | `/market/benchmarks` | Benchmarks P25/P50/P75/P90 |

### Valuation (`/valuation`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/valuation/events` | Lista valuation events |
| GET | `/valuation/events/{event_id}` | Detalle con multiple_analyses |
| POST | `/valuation/analyze` | Ejecuta análisis — require_analyst |
| GET | `/valuation/drivers/{startup_id}` | Drivers de valoración |
| GET | `/valuation/outliers` | Outlier flags |

### Fund (`/fund`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/fund` | Datos del fondo activo |
| GET | `/fund/investments` | Inversiones con nombre de startup |
| GET | `/fund/metrics` | Métricas actuales (último FundMetric) |
| GET | `/fund/scenarios` | Escenarios Monte Carlo guardados |
| POST | `/fund/simulate` | Ejecuta Monte Carlo — require_gp |
| GET | `/fund/simulate/quick` | Monte Carlo con preset (conservador/base/optimista) |

### Studio (`/studio`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/studio/summary` | Resumen del portfolio del studio |
| GET | `/studio/companies` | Lista empresas con startup_name y fase |
| GET | `/studio/companies/{id}` | Detalle de empresa del studio |
| GET | `/studio/companies/{name}/timeline` | Línea de tiempo cronológica |
| GET | `/studio/companies/{name}/costs` | Breakdown de build_costs |
| GET | `/studio/companies/{name}/milestones` | Hitos con estado achieved |
| GET | `/studio/alpha` | Alpha metrics donde studio > mercado |
| GET | `/studio/alpha/score/{id}` | Score de alpha 0–100 |

### Fintech (`/fintech`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/fintech/subverticals` | Lista subverticales con filtros |
| GET | `/fintech/subverticals/{id}` | Detalle con FintechSubverticalSummary |
| GET | `/fintech/overview` | FintechMarketOverview |
| GET | `/fintech/unit-economics` | Unit economics por startup/subvertical |
| GET | `/fintech/comparables` | Comparables por subvertical/geography |
| GET | `/fintech/regulatory-risks` | Riesgos regulatorios |

### Deals (`/deals`) y Sourcing (`/sourcing`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/deals` | Lista deals con filtros |
| GET | `/deals/summary` | Estadísticas del pipeline |
| GET | `/deals/{deal_id}` | Deal completo con thesis, DD e IC memos |
| GET | `/deals/{deal_id}/thesis` | Thesis alignments con score total |
| GET | `/deals/{deal_id}/checklist` | DD checklist con progreso por categoría |
| GET | `/deals/{deal_id}/memos` | IC memos ordenados por version desc |
| GET | `/sourcing/channels` | Canales de sourcing activos |
| GET | `/sourcing/channels/{channel_id}/deals` | Deals de un canal específico |

### Reports (`/reports`)
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/reports/lp-summary` | Resumen ejecutivo LP — require_gp |
| GET | `/reports/portfolio-snapshot` | Snapshot por startup — ARR, MRR, NRR, burn, runway |
| GET | `/reports/ic-decisions` | Decisiones IC ordenadas por fecha |
| GET | `/reports/pipeline-status` | Estado del pipeline con days_in_pipeline |

---

## Frontend — 7 secciones

| Ruta | Sección |
|---|---|
| `/` | Dashboard — KPIs ejecutivos, portafolio, studio, pipeline |
| `/portfolio` | Lista de startups con filtros |
| `/portfolio/[name]` | Detalle de startup — ARR histórico, percentil |
| `/fund` | Fund Simulator — Monte Carlo MOIC/IRR |
| `/studio` | Venture Studio — alpha metrics, build cost |
| `/deals` | Deal Pipeline — sourcing, thesis scores |
| `/market` | Benchmarks de mercado por segmento |
| `/reports` | LP Report — snapshot del portafolio |

### Paleta de colores institucional

| Variable | Hex | Uso |
|---|---|---|
| `--navy` | `#0B1628` | Sidebar, fondo principal |
| `--accent` | `#1A6FE8` | CTAs, highlights, badges |
| `--success` | `#22C55E` | Métricas positivas |
| `--warning` | `#F5A623` | Alertas, burn alto |
| `--danger` | `#EF4444` | Métricas negativas |
| `--secondary` | `#9CA3AF` | Textos secundarios, bordes |

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
| Fondo | AIDA Ventures Fund I |
| Etapas objetivo | Pre-Seed / Seed / Series A |
| Geografía foco | Colombia (foco) + LATAM |
| Sectores core | Fintech, SaaS, LogTech |
| Venture Studio | Activo — el sistema mide alpha vs mercado |
| Tamaño del fondo | Parámetro ajustable (default demo: $10M) |
| Startups en portafolio real | 0 — sistema en modo demo con datos simulados |
| Empresas studio reales | 0 — sistema en modo demo con datos simulados |
| Modo actual | Demo — datos 100% ficticios |

---

*Última actualización: Abril 2026 — AIDA Ventures*
*Estado: Fase 4 completa — backend 57 rutas + frontend Next.js 7 secciones operativas*
*Base de datos: 43 tablas — 503 registros simulados cargados*
