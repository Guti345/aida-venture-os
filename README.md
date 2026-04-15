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

> **Fase: Demo funcional con datos simulados**
> El sistema opera con datos inventados para validar arquitectura, flujos y visualizaciones.
> Los datos reales se integrarán en una segunda fase mediante formularios de reporte periódico.

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

El sistema arranca con **147 registros simulados** distribuidos así:

### Portafolio externo (5 startups)

| Startup | Sector | Etapa | ARR simulado | País |
|---|---|---|---|---|
| FinStack | Fintech / Neobank B2B | Seed | $480K | Colombia |
| LogiFlow | LogTech / Last-mile SaaS | Series A | $3.2M | México |
| MediSync | HealthTech / SaaS clínico | Pre-Seed | $36K | Colombia |
| CreditIA | Fintech / Digital Lending | Seed | $620K | Colombia |
| AgriSense | AgriTech / Precision farming | Seed | $390K | Colombia |

### Venture studio (5 empresas simuladas)

| Empresa | Sector | Etapa studio | Estado |
|---|---|---|---|
| EduStack | EdTech / SaaS B2B | MVP | En construcción |
| LegalBot | LegalTech / AI | Validación | En construcción |
| FleetOS | LogTech / Gestión flotillas | PMF | Graduada a Seed externo |
| InsureX | InsurTech / Embedded | Idea | En construcción |
| TaxFlow | FinTech / Contabilidad PYME | Validación | En construcción |

> **Nota:** Todos estos datos son ficticios y serán reemplazados con información real
> cuando el fondo y el studio comiencen operaciones con startups reales.

### Plan de transición datos simulados → datos reales

```
Fase demo (hoy)     → Datos inventados en seed_data.py y studio_seed_data.py
Fase piloto         → GP ingresa datos manualmente via formulario en el sistema
Fase operacional    → Startups reportan via formulario mensual (Google Form o UI propia)
Fase automatizada   → Integración directa con fuentes (contabilidad, CRM, bancos)
```

---

## Roles y perfiles de usuario

El sistema tiene **3 perfiles de acceso** con permisos diferenciados:

| Perfil | Acceso | Capacidades |
|---|---|---|
| `gp` | Total | Todas las vistas, simulador del fondo, configuración |
| `analyst` | Lectura + entrada de datos | Startups, métricas, deals, reportes — sin simulador ni configuración del fondo |
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
│   ├── main.py                  # Entry point — FastAPI app
│   ├── database.py              # Conexión y sesión PostgreSQL
│   │
│   ├── models/                  # Modelos SQLAlchemy — 43 tablas totales
│   │   ├── __init__.py
│   │   ├── shared.py            # users, currencies, tags, audit_logs
│   │   ├── market.py            # market_segments, benchmark_entries, benchmark_series, valuation_distributions
│   │   ├── startup.py           # startups, founders, startup_founders, funding_rounds, metric_snapshots, cohort_analyses
│   │   ├── valuation.py         # valuation_events, multiple_analyses, valuation_drivers, outlier_flags
│   │   ├── fund.py              # funds, lps, investments, portfolio_allocations, deal_assumptions, fund_scenarios, fund_metrics
│   │   ├── studio.py            # studio_companies, build_costs, studio_milestones, alpha_metrics
│   │   ├── fintech.py           # fintech_subverticals, fintech_unit_economics, regulatory_risks, fintech_comparables
│   │   ├── dealflow.py          # deal_opportunities, thesis_alignments, sourcing_channels, dd_checklists, ic_memos
│   │   └── reporting.py         # lp_profiles, reports, narrative_blocks, ic_decisions
│   │
│   ├── schemas/                 # Pydantic schemas — validación de entrada y salida
│   │   ├── __init__.py
│   │   ├── market.py
│   │   ├── startup.py
│   │   ├── valuation.py
│   │   ├── fund.py
│   │   ├── studio.py
│   │   ├── fintech.py
│   │   ├── dealflow.py
│   │   └── reporting.py
│   │
│   ├── routers/                 # Endpoints REST por dominio
│   │   ├── __init__.py
│   │   ├── market.py            # GET /benchmarks, GET /segments
│   │   ├── startups.py          # CRUD startups + métricas
│   │   ├── valuation.py         # POST /valuation/analyze
│   │   ├── fund.py              # GET /fund/metrics, POST /fund/scenario
│   │   ├── studio.py            # GET /studio/alpha
│   │   ├── fintech.py           # GET /fintech/subverticals
│   │   ├── dealflow.py          # CRUD deals + pipeline
│   │   └── reporting.py         # POST /reports/generate
│   │
│   └── services/                # Lógica de negocio pura
│       ├── __init__.py
│       ├── percentile.py        # Startup X en percentil Y vs benchmark Z
│       ├── simulator.py         # Monte Carlo — distribución MOIC/IRR
│       ├── alpha.py             # Studio alpha vs mercado
│       └── importer.py          # Importación de Excels / formularios a DB
│
├── alembic/                     # Migraciones de base de datos
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                # Archivos de migración generados
│
├── data/                        # Datos semilla para desarrollo
│   ├── seed_data.py             # 5 startups portafolio + fondo + inversiones (147 registros)
│   ├── studio_seed_data.py      # 5 empresas venture studio simuladas
│   ├── benchmarks_seed.py       # Benchmarks externos LATAM/US desde Excels
│   ├── VCFunds_Metrics.xlsx
│   ├── Venture_Studio_Metrics_Reference.xlsx
│   ├── _AIDA_Ventures_-_Startups_Benchmarks.xlsx
│   ├── _Metricas_Startups.xlsx
│   └── Fintech_Sectors.xlsx
│
├── tests/                       # Tests por dominio
│   ├── test_market.py
│   ├── test_startups.py
│   ├── test_valuation.py
│   └── test_simulator.py
│
├── .env                         # Credenciales reales — NO subir a GitHub
├── .env.example                 # Template público de credenciales
├── requirements.txt             # Dependencias del proyecto
├── alembic.ini                  # Configuración de Alembic
└── README.md                    # Este archivo
```

---

## Base de datos — 43 tablas en 8 dominios

### Dominio 0 — Transversales (4 tablas)

| Tabla | Propósito |
|---|---|
| `users` | Usuarios del sistema con roles: gp / analyst / studio_operator / viewer |
| `currencies` | Tipos de cambio vs USD |
| `tags` | Etiquetas reutilizables para startups y deals |
| `audit_logs` | Historial completo de cambios — quién cambió qué y cuándo |

### Dominio 1 — Market Reality Layer (4 tablas)

| Tabla | Propósito |
|---|---|
| `market_segments` | Combinación [sector × etapa × geografía] |
| `benchmark_entries` | Percentiles P10/P25/P50/P75/P90 por segmento y múltiplo |
| `benchmark_series` | Evolución temporal de múltiplos |
| `valuation_distributions` | Distribución completa de valoraciones por segmento |

### Dominio 2 — Startup Engine (7 tablas)

| Tabla | Propósito |
|---|---|
| `founders` | Perfil de fundadores |
| `startups` | Entidad central — portafolio externo y studio |
| `startup_founders` | Relación startup ↔ fundador con equity |
| `startup_tags` | Etiquetas asociadas a startups |
| `funding_rounds` | Rondas de financiación históricas |
| `metric_snapshots` | Serie temporal de métricas (ARR, burn, CAC, LTV…) |
| `cohort_analyses` | Retención de clientes por cohorte |

### Dominio 3 — Valuation Intelligence (4 tablas)

| Tabla | Propósito |
|---|---|
| `valuation_events` | Valoración registrada en cada ronda |
| `multiple_analyses` | Múltiplo pagado vs percentiles del mercado |
| `valuation_drivers` | Factores que justifican premium (NRR, Rule of 40…) |
| `outlier_flags` | Detección automática de sobre/infravaloración |

### Dominio 4 — Fund Construction Simulator (7 tablas)

| Tabla | Propósito |
|---|---|
| `funds` | Parámetros maestros del fondo — tamaño ajustable |
| `lps` | Limited Partners con compromisos de capital |
| `investments` | Inversiones realizadas |
| `portfolio_allocations` | Distribución target vs real por etapa/sector |
| `deal_assumptions` | Supuestos por deal (ticket, dilución, exit múltiplo) |
| `fund_scenarios` | Escenarios Base / High / Downside con MOIC e IRR |
| `fund_metrics` | MOIC, TVPI, DPI, RVPI, IRR calculados |

### Dominio 5 — Studio Performance (4 tablas)

| Tabla | Propósito |
|---|---|
| `studio_companies` | Empresas construidas por el studio con línea de tiempo |
| `build_costs` | Costo de construcción por categoría y período |
| `studio_milestones` | Hitos: Idea → Validación → MVP → PMF → Seed externo |
| `alpha_metrics` | Comparación studio vs mercado en indicadores clave |

### Dominio 6 — Fintech Deep Dive (4 tablas)

| Tabla | Propósito |
|---|---|
| `fintech_subverticals` | Payments, Neobanks, Lending, BaaS, InsurTech, WealthTech |
| `fintech_unit_economics` | Métricas específicas por modelo (NPL, TPV, NIM) |
| `regulatory_risks` | Riesgos regulatorios por mercado y estado |
| `fintech_comparables` | Peers de referencia por subvertical |

### Dominio 7 — Deal Flow & Sourcing (5 tablas)

| Tabla | Propósito |
|---|---|
| `deal_opportunities` | Deal en pipeline: Identified → Screening → DD → IC → Invested |
| `thesis_alignments` | Score de alineación con tesis del fondo |
| `sourcing_channels` | Origen de deals (red, aceleradoras, inbound, studio) |
| `dd_checklists` | Due diligence por categoría |
| `ic_memos` | Memos de Investment Committee versionados |

### Dominio 8 — Reporting & LP Intelligence (4 tablas)

| Tabla | Propósito |
|---|---|
| `lp_profiles` | Preferencias y tier de cada LP |
| `reports` | Reportes generados (IC memo, LP update, PPM, sourcing deck) |
| `narrative_blocks` | Bloques de texto con datos reales incrustados |
| `ic_decisions` | Registro de decisiones con justificación y snapshot de datos |

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

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
# 1. Activar entorno virtual (hacer esto siempre al abrir VS Code)
.\venv\Scripts\activate

# 2. Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# 3. Correr migraciones — crea las 43 tablas en PostgreSQL
alembic upgrade head

# 4. Cargar datos simulados — portafolio externo
python data/seed_data.py

# 5. Cargar datos simulados — venture studio
python data/studio_seed_data.py

# 6. Cargar benchmarks desde Excels
python data/benchmarks_seed.py

# 7. Iniciar el servidor
uvicorn app.main:app --reload
```

Disponible en:
- `http://localhost:8000` — API
- `http://localhost:8000/docs` — Swagger UI (documentación interactiva)
- `http://localhost:8000/redoc` — ReDoc

---

## Plan de desarrollo por fases

### Fase 0 — Fundaciones (semanas 1–2) ← ESTAMOS AQUÍ
- [ ] Estructura de carpetas del proyecto
- [ ] `database.py` — conexión PostgreSQL
- [ ] Modelos SQLAlchemy — las 43 tablas
- [ ] Migraciones Alembic
- [ ] `main.py` — FastAPI con health check
- [ ] Cargar datos simulados (seed_data.py + studio_seed_data.py)

### Fase 1 — Motor de comparabilidad (semanas 3–5)
- [ ] APIs Market Reality + Startup Engine
- [ ] Servicio percentile.py — startup X en percentil Y vs benchmark
- [ ] Importador de Excels a DB
- [ ] Benchmarks seed cargados

### Fase 2 — Simulador y studio (semanas 6–8)
- [ ] Valuation Intelligence — APIs + lógica
- [ ] Fund Simulator — Monte Carlo MOIC/IRR con fondo parametrizable
- [ ] Studio Performance — alpha vs mercado
- [ ] Fintech Deep Dive

### Fase 3 — Demo completo (semanas 9–10)
- [ ] Deal Flow & Sourcing
- [ ] Reporting — generador de LP reports
- [ ] Sistema de roles (gp / analyst / studio_operator / viewer)
- [ ] Formulario de ingesta de métricas para startups
- [ ] Tests por dominio

### Fase 4 — Transición a datos reales (post-demo)
- [ ] Reemplazar seed data por datos reales del fondo
- [ ] Proceso de reporte periódico con startups reales
- [ ] Onboarding de primeros LPs como viewers

---

## Reglas de desarrollo

1. **No promedios — siempre percentiles.** Toda comparación usa P25/P50/P75/P90.
2. **Toda métrica tiene fecha y fuente.** Sin `reference_date` y `source` no se guarda.
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
| Venture Studio | Activo — mide alpha vs mercado |
| Tamaño del fondo | Parámetro ajustable (default demo: $10M) |
| Startups en portafolio real | 0 — sistema en modo demo con datos simulados |
| Empresas studio reales | 0 — sistema en modo demo con datos simulados |
| Usuarios del sistema | GPs y analistas internos + operadores del studio |
| Objetivo inmediato | Demo funcional para BI y reportes LP |

---

## Datos seed disponibles

### Archivos Excel (benchmarks externos)

| Archivo | Tablas destino | Registros est. |
|---|---|---|
| `VCFunds_Metrics.xlsx` | `benchmark_entries`, `market_segments` | ~80 |
| `Venture_Studio_Metrics_Reference.xlsx` | `alpha_metrics` (benchmarks) | ~40 |
| `_AIDA_Ventures_-_Startups_Benchmarks.xlsx` | `benchmark_entries`, `valuation_distributions` | ~200 |
| `_Metricas_Startups.xlsx` | `benchmark_entries`, `market_segments` | ~150 |
| `Fintech_Sectors.xlsx` | `fintech_subverticals`, `benchmark_entries` | ~80 |

### Datos simulados (generados para desarrollo)

| Archivo | Contenido | Registros |
|---|---|---|
| `data/seed_data.py` | 5 startups portafolio + fondo + métricas + inversiones | 147 |
| `data/studio_seed_data.py` | 5 empresas venture studio + costos + hitos | ~80 |
| `data/benchmarks_seed.py` | Benchmarks LATAM/US normalizados desde Excels | ~550 |

---

*Última actualización: Abril 2026 — AIDA Ventures*
*Estado: Modo demo — datos 100% simulados*