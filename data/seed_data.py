"""
AIDA Venture OS — Seed Data
5 startups simuladas para desarrollo del software.
Reemplazar con datos reales cuando estén disponibles.

Ejecutar: python seed_data.py
Requiere: DATABASE_URL en .env y tablas creadas con alembic upgrade head
"""

FUND = {
    "id": "fund-001",
    "name": "AIDA Ventures Fund I",
    "vintage_year": 2022,
    "target_size_usd": 10_000_000,
    "deployed_usd": 3_650_000,
    "currency": "USD",
    "geography_focus": "LATAM",
    "stage_focus": "Pre-Seed / Seed",
    "status": "investing"
}

STARTUPS = [
    {
        "id": "startup-001",
        "name": "FinStack",
        "sector": "Fintech",
        "subsector": "Neobank B2B",
        "stage": "Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Bogotá",
        "founded_at": "2022-03-15",
        "studio_built": False,
        "website": "finstack.co",
        "description": (
            "Neobank B2B para PYMEs colombianas. Cuenta empresarial digital "
            "con crédito embebido, nómina y pagos internacionales. "
            "Modelo de ingresos: SaaS + interchange fees."
        ),
        "status": "active"
    },
    {
        "id": "startup-002",
        "name": "LogiFlow",
        "sector": "LogTech",
        "subsector": "Last-mile logistics SaaS",
        "stage": "Series A",
        "geography": "LATAM",
        "country": "MX",
        "city": "Ciudad de México",
        "founded_at": "2021-07-01",
        "studio_built": False,
        "website": "logiflow.mx",
        "description": (
            "SaaS de optimización de rutas y gestión de última milla "
            "para retailers y e-commerce en México y Colombia. "
            "Modelo: licencia anual por vehículo + revenue share."
        ),
        "status": "active"
    },
    {
        "id": "startup-003",
        "name": "MediSync",
        "sector": "HealthTech",
        "subsector": "SaaS clínico",
        "stage": "Pre-Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Medellín",
        "founded_at": "2023-09-01",
        "studio_built": True,
        "website": "medisync.co",
        "description": (
            "Plataforma de gestión clínica para consultorios y clínicas medianas. "
            "Historia clínica digital, agenda inteligente y telemedicina. "
            "Modelo: SaaS mensual por sede + módulos adicionales."
        ),
        "status": "active"
    },
    {
        "id": "startup-004",
        "name": "CreditIA",
        "sector": "Fintech",
        "subsector": "Digital Lending",
        "stage": "Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Bogotá",
        "founded_at": "2022-11-10",
        "studio_built": True,
        "website": "creditia.co",
        "description": (
            "Motor de scoring crediticio con IA para población sin historial bancario. "
            "Crédito de consumo y capital de trabajo. "
            "Modelo: spread sobre tasa + origination fee."
        ),
        "status": "active"
    },
    {
        "id": "startup-005",
        "name": "AgriSense",
        "sector": "AgriTech",
        "subsector": "Precision farming SaaS",
        "stage": "Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Cali",
        "founded_at": "2022-06-20",
        "studio_built": False,
        "website": "agrisense.co",
        "description": (
            "SaaS de agricultura de precisión para medianos productores. "
            "IoT + ML para optimización de riego, fertilización y cosecha. "
            "Modelo: SaaS anual por hectárea + hardware IoT (lease)."
        ),
        "status": "active"
    },
]

FOUNDERS = [
    # FinStack
    {"id":"f-001","startup_id":"startup-001","name":"Valentina Ríos","role":"CEO","email":"v.rios@finstack.co","equity_pct":35.0,
     "background":"Ex VP Bancolombia Digital. MBA Uniandes. 8 años en banca digital y productos financieros para PYMEs."},
    {"id":"f-002","startup_id":"startup-001","name":"Andrés Mora","role":"CTO","email":"a.mora@finstack.co","equity_pct":30.0,
     "background":"Ex tech lead Nubank Brasil. Ingeniero de sistemas Javeriana. Especialista en sistemas de pago y core banking."},
    # LogiFlow
    {"id":"f-003","startup_id":"startup-002","name":"Carlos Mendoza","role":"CEO","email":"c.mendoza@logiflow.mx","equity_pct":40.0,
     "background":"Ex director de operaciones DHL México. MBA IPADE. 12 años en logística y cadena de suministro."},
    {"id":"f-004","startup_id":"startup-002","name":"Sofía Herrera","role":"CPO","email":"s.herrera@logiflow.mx","equity_pct":25.0,
     "background":"Ex product manager Rappi (growth). Ingeniera industrial ITAM. Especialista en marketplace logistics."},
    # MediSync
    {"id":"f-005","startup_id":"startup-003","name":"Dr. Julián Ospina","role":"CEO","email":"j.ospina@medisync.co","equity_pct":45.0,
     "background":"Médico Universidad de Antioquia + MSc Health Informatics King's College. 5 años en gestión clínica."},
    {"id":"f-006","startup_id":"startup-003","name":"Mariana Castro","role":"CTO","email":"m.castro@medisync.co","equity_pct":30.0,
     "background":"Ingeniera de software U. EAFIT. Ex Globant (healthcare vertical). Especialista en interoperabilidad HL7/FHIR."},
    # CreditIA
    {"id":"f-007","startup_id":"startup-004","name":"Felipe Arango","role":"CEO","email":"f.arango@creditia.co","equity_pct":40.0,
     "background":"Ex gerente de riesgo de crédito Bancolombia. Economista + MSc Data Science Uniandes. 9 años en riesgo financiero."},
    {"id":"f-008","startup_id":"startup-004","name":"Isabel Torres","role":"CTO","email":"i.torres@creditia.co","equity_pct":30.0,
     "background":"Ex ML engineer Rappi (fraud & risk). PhD(c) Inteligencia Artificial Universidad Nacional."},
    # AgriSense
    {"id":"f-009","startup_id":"startup-005","name":"Diego Salcedo","role":"CEO","email":"d.salcedo@agrisense.co","equity_pct":38.0,
     "background":"Ingeniero agrónomo U. Nacional + MBA. Familia cafetera 3ra generación. Ex consultor McKinsey (sector agrícola)."},
    {"id":"f-010","startup_id":"startup-005","name":"Paula Jiménez","role":"CTO","email":"p.jimenez@agrisense.co","equity_pct":28.0,
     "background":"Ingeniera electrónica U. del Valle + MSc IoT KU Leuven. Ex Siemens Colombia. Especialista en sensores y edge computing."},
]

FUNDING_ROUNDS = [
    {"id":"r-001","startup_id":"startup-001","round_type":"pre_seed","amount_usd":150_000,"pre_money_val":1_500_000,"post_money_val":1_650_000,"lead_investor":"AIDA Ventures","date":"2022-09-01","status":"closed"},
    {"id":"r-002","startup_id":"startup-001","round_type":"seed","amount_usd":800_000,"pre_money_val":6_000_000,"post_money_val":6_800_000,"lead_investor":"AIDA Ventures","date":"2023-06-15","status":"closed"},
    {"id":"r-003","startup_id":"startup-002","round_type":"seed","amount_usd":1_200_000,"pre_money_val":7_500_000,"post_money_val":8_700_000,"lead_investor":"AIDA Ventures","date":"2022-02-01","status":"closed"},
    {"id":"r-004","startup_id":"startup-002","round_type":"series_a","amount_usd":4_500_000,"pre_money_val":22_000_000,"post_money_val":26_500_000,"lead_investor":"Kaszek Ventures","date":"2023-11-01","status":"closed"},
    {"id":"r-005","startup_id":"startup-003","round_type":"pre_seed","amount_usd":120_000,"pre_money_val":1_200_000,"post_money_val":1_320_000,"lead_investor":"AIDA Ventures Studio","date":"2023-12-01","status":"closed"},
    {"id":"r-006","startup_id":"startup-004","round_type":"pre_seed","amount_usd":180_000,"pre_money_val":1_800_000,"post_money_val":1_980_000,"lead_investor":"AIDA Ventures Studio","date":"2023-03-01","status":"closed"},
    {"id":"r-007","startup_id":"startup-004","round_type":"seed","amount_usd":750_000,"pre_money_val":5_500_000,"post_money_val":6_250_000,"lead_investor":"AIDA Ventures","date":"2024-01-15","status":"closed"},
    {"id":"r-008","startup_id":"startup-005","round_type":"pre_seed","amount_usd":200_000,"pre_money_val":2_000_000,"post_money_val":2_200_000,"lead_investor":"AIDA Ventures","date":"2022-11-01","status":"closed"},
    {"id":"r-009","startup_id":"startup-005","round_type":"seed","amount_usd":900_000,"pre_money_val":7_000_000,"post_money_val":7_900_000,"lead_investor":"AIDA Ventures","date":"2024-03-01","status":"closed"},
]

# Métricas mensuales por startup — serie temporal completa
METRIC_SNAPSHOTS = [
    # ═══ FINSTACK — Neobank B2B — Seed ═══
    {"startup_id":"startup-001","metric_name":"MRR","value":5_000,"unit":"USD","currency":"USD","period_date":"2023-03-01"},
    {"startup_id":"startup-001","metric_name":"MRR","value":7_000,"unit":"USD","currency":"USD","period_date":"2023-06-01"},
    {"startup_id":"startup-001","metric_name":"MRR","value":9_000,"unit":"USD","currency":"USD","period_date":"2023-09-01"},
    {"startup_id":"startup-001","metric_name":"MRR","value":12_000,"unit":"USD","currency":"USD","period_date":"2023-12-01"},
    {"startup_id":"startup-001","metric_name":"MRR","value":16_000,"unit":"USD","currency":"USD","period_date":"2024-03-01"},
    {"startup_id":"startup-001","metric_name":"MRR","value":24_000,"unit":"USD","currency":"USD","period_date":"2024-06-01"},
    {"startup_id":"startup-001","metric_name":"MRR","value":32_000,"unit":"USD","currency":"USD","period_date":"2024-09-01"},
    {"startup_id":"startup-001","metric_name":"MRR","value":40_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"ARR","value":480_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"YoY_growth_pct","value":233,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"burn_rate_monthly","value":85_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"runway_months","value":18,"unit":"months","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"burn_multiple","value":1.7,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"gross_margin_pct","value":62,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"active_customers","value":320,"unit":"companies","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"CAC","value":1_200,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"LTV","value":8_400,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"LTV_CAC_ratio","value":7.0,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"NRR_pct","value":118,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"GRR_pct","value":91,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"CAC_payback_months","value":17,"unit":"months","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-001","metric_name":"headcount","value":18,"unit":"people","currency":None,"period_date":"2024-12-01"},
    # ═══ LOGIFLOW — LogTech SaaS — Series A ═══
    {"startup_id":"startup-002","metric_name":"MRR","value":40_000,"unit":"USD","currency":"USD","period_date":"2023-03-01"},
    {"startup_id":"startup-002","metric_name":"MRR","value":60_000,"unit":"USD","currency":"USD","period_date":"2023-06-01"},
    {"startup_id":"startup-002","metric_name":"MRR","value":80_000,"unit":"USD","currency":"USD","period_date":"2023-09-01"},
    {"startup_id":"startup-002","metric_name":"MRR","value":80_000,"unit":"USD","currency":"USD","period_date":"2023-12-01"},
    {"startup_id":"startup-002","metric_name":"MRR","value":115_000,"unit":"USD","currency":"USD","period_date":"2024-03-01"},
    {"startup_id":"startup-002","metric_name":"MRR","value":160_000,"unit":"USD","currency":"USD","period_date":"2024-06-01"},
    {"startup_id":"startup-002","metric_name":"MRR","value":210_000,"unit":"USD","currency":"USD","period_date":"2024-09-01"},
    {"startup_id":"startup-002","metric_name":"MRR","value":267_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"ARR","value":3_200_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"YoY_growth_pct","value":134,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"burn_rate_monthly","value":310_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"runway_months","value":26,"unit":"months","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"burn_multiple","value":1.4,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"gross_margin_pct","value":71,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"active_customers","value":87,"unit":"companies","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"CAC","value":18_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"LTV","value":198_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"LTV_CAC_ratio","value":11.0,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"NRR_pct","value":124,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"GRR_pct","value":94,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"CAC_payback_months","value":14,"unit":"months","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-002","metric_name":"headcount","value":52,"unit":"people","currency":None,"period_date":"2024-12-01"},
    # ═══ MEDISYNC — HealthTech SaaS — Pre-Seed (Studio) ═══
    {"startup_id":"startup-003","metric_name":"MRR","value":600,"unit":"USD","currency":"USD","period_date":"2024-03-01"},
    {"startup_id":"startup-003","metric_name":"MRR","value":1_200,"unit":"USD","currency":"USD","period_date":"2024-06-01"},
    {"startup_id":"startup-003","metric_name":"MRR","value":1_800,"unit":"USD","currency":"USD","period_date":"2024-09-01"},
    {"startup_id":"startup-003","metric_name":"MRR","value":3_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"ARR","value":36_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"YoY_growth_pct","value":400,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"burn_rate_monthly","value":22_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"runway_months","value":14,"unit":"months","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"gross_margin_pct","value":78,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"active_customers","value":28,"unit":"clinics","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"CAC","value":800,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"LTV","value":7_200,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"LTV_CAC_ratio","value":9.0,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"NRR_pct","value":108,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-003","metric_name":"headcount","value":7,"unit":"people","currency":None,"period_date":"2024-12-01"},
    # ═══ CREDITIA — Fintech Lending — Seed (Studio) ═══
    {"startup_id":"startup-004","metric_name":"MRR","value":2_000,"unit":"USD","currency":"USD","period_date":"2023-06-01"},
    {"startup_id":"startup-004","metric_name":"MRR","value":5_000,"unit":"USD","currency":"USD","period_date":"2023-09-01"},
    {"startup_id":"startup-004","metric_name":"MRR","value":10_000,"unit":"USD","currency":"USD","period_date":"2023-12-01"},
    {"startup_id":"startup-004","metric_name":"MRR","value":24_000,"unit":"USD","currency":"USD","period_date":"2024-03-01"},
    {"startup_id":"startup-004","metric_name":"MRR","value":38_000,"unit":"USD","currency":"USD","period_date":"2024-06-01"},
    {"startup_id":"startup-004","metric_name":"MRR","value":38_000,"unit":"USD","currency":"USD","period_date":"2024-09-01"},
    {"startup_id":"startup-004","metric_name":"MRR","value":51_700,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"ARR","value":620_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"YoY_growth_pct","value":517,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"burn_rate_monthly","value":110_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"runway_months","value":20,"unit":"months","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"burn_multiple","value":2.1,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"gross_margin_pct","value":55,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"active_customers","value":4_800,"unit":"borrowers","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"CAC","value":45,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"LTV","value":290,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"LTV_CAC_ratio","value":6.4,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"NPL_rate_pct","value":4.2,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"NRR_pct","value":105,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-004","metric_name":"headcount","value":22,"unit":"people","currency":None,"period_date":"2024-12-01"},
    # ═══ AGRISENSE — AgriTech SaaS — Seed ═══
    {"startup_id":"startup-005","metric_name":"MRR","value":5_000,"unit":"USD","currency":"USD","period_date":"2023-06-01"},
    {"startup_id":"startup-005","metric_name":"MRR","value":7_500,"unit":"USD","currency":"USD","period_date":"2023-09-01"},
    {"startup_id":"startup-005","metric_name":"MRR","value":9_000,"unit":"USD","currency":"USD","period_date":"2023-12-01"},
    {"startup_id":"startup-005","metric_name":"MRR","value":9_000,"unit":"USD","currency":"USD","period_date":"2024-03-01"},
    {"startup_id":"startup-005","metric_name":"MRR","value":16_000,"unit":"USD","currency":"USD","period_date":"2024-06-01"},
    {"startup_id":"startup-005","metric_name":"MRR","value":24_000,"unit":"USD","currency":"USD","period_date":"2024-09-01"},
    {"startup_id":"startup-005","metric_name":"MRR","value":32_500,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"ARR","value":390_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"YoY_growth_pct","value":261,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"burn_rate_monthly","value":95_000,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"runway_months","value":22,"unit":"months","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"burn_multiple","value":2.9,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"gross_margin_pct","value":68,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"active_customers","value":145,"unit":"farms","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"CAC","value":2_200,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"LTV","value":14_400,"unit":"USD","currency":"USD","period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"LTV_CAC_ratio","value":6.5,"unit":"ratio","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"NRR_pct","value":112,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"GRR_pct","value":89,"unit":"pct","currency":None,"period_date":"2024-12-01"},
    {"startup_id":"startup-005","metric_name":"headcount","value":19,"unit":"people","currency":None,"period_date":"2024-12-01"},
]

INVESTMENTS = [
    {"startup_id":"startup-001","fund_id":"fund-001","round_id":"r-001","amount_usd":150_000,"pre_money_val":1_500_000,"equity_pct":9.09,"date":"2022-09-01","investment_type":"lead","follow_on_reserve_usd":500_000},
    {"startup_id":"startup-001","fund_id":"fund-001","round_id":"r-002","amount_usd":500_000,"pre_money_val":6_000_000,"equity_pct":7.35,"date":"2023-06-15","investment_type":"follow_on","follow_on_reserve_usd":0},
    {"startup_id":"startup-002","fund_id":"fund-001","round_id":"r-003","amount_usd":600_000,"pre_money_val":7_500_000,"equity_pct":6.9,"date":"2022-02-01","investment_type":"lead","follow_on_reserve_usd":500_000},
    {"startup_id":"startup-002","fund_id":"fund-001","round_id":"r-004","amount_usd":500_000,"pre_money_val":22_000_000,"equity_pct":1.89,"date":"2023-11-01","investment_type":"co_invest","follow_on_reserve_usd":0},
    {"startup_id":"startup-003","fund_id":"fund-001","round_id":"r-005","amount_usd":120_000,"pre_money_val":1_200_000,"equity_pct":9.09,"date":"2023-12-01","investment_type":"lead","follow_on_reserve_usd":300_000},
    {"startup_id":"startup-004","fund_id":"fund-001","round_id":"r-006","amount_usd":180_000,"pre_money_val":1_800_000,"equity_pct":9.09,"date":"2023-03-01","investment_type":"lead","follow_on_reserve_usd":400_000},
    {"startup_id":"startup-004","fund_id":"fund-001","round_id":"r-007","amount_usd":400_000,"pre_money_val":5_500_000,"equity_pct":6.4,"date":"2024-01-15","investment_type":"follow_on","follow_on_reserve_usd":0},
    {"startup_id":"startup-005","fund_id":"fund-001","round_id":"r-008","amount_usd":200_000,"pre_money_val":2_000_000,"equity_pct":9.09,"date":"2022-11-01","investment_type":"lead","follow_on_reserve_usd":500_000},
    {"startup_id":"startup-005","fund_id":"fund-001","round_id":"r-009","amount_usd":500_000,"pre_money_val":7_000_000,"equity_pct":6.33,"date":"2024-03-01","investment_type":"follow_on","follow_on_reserve_usd":0},
]

STUDIO_COMPANIES = [
    {
        "startup_id": "startup-003",
        "idea_date": "2023-07-01",
        "validation_date": "2023-09-15",
        "mvp_date": "2023-11-01",
        "pmf_date": None,
        "first_external_seed_date": None,
        "build_cost_usd": 95_000,
        "equity_retained_pct": 45.0,
        "studio_support_level": "full",
        "notes": "Primera empresa del studio en sector salud. Validación en 2.5 meses — récord interno."
    },
    {
        "startup_id": "startup-004",
        "idea_date": "2022-10-01",
        "validation_date": "2022-12-15",
        "mvp_date": "2023-02-01",
        "pmf_date": "2023-10-01",
        "first_external_seed_date": "2024-01-15",
        "build_cost_usd": 140_000,
        "equity_retained_pct": 40.0,
        "studio_support_level": "full",
        "notes": "Primera empresa del studio en llegar a PMF y levantar ronda externa. Referencia de alpha para el modelo."
    },
]

DEAL_ASSUMPTIONS = [
    {"startup_id":"startup-001","fund_id":"fund-001","ticket_usd":650_000,"target_ownership_pct":16.44,"dilution_per_round_pct":20,"expected_exit_multiple":12,"expected_exit_years":6,"follow_on_pct":25},
    {"startup_id":"startup-002","fund_id":"fund-001","ticket_usd":1_100_000,"target_ownership_pct":8.79,"dilution_per_round_pct":20,"expected_exit_multiple":8,"expected_exit_years":5,"follow_on_pct":20},
    {"startup_id":"startup-003","fund_id":"fund-001","ticket_usd":120_000,"target_ownership_pct":9.09,"dilution_per_round_pct":25,"expected_exit_multiple":15,"expected_exit_years":7,"follow_on_pct":30},
    {"startup_id":"startup-004","fund_id":"fund-001","ticket_usd":580_000,"target_ownership_pct":15.49,"dilution_per_round_pct":22,"expected_exit_multiple":10,"expected_exit_years":6,"follow_on_pct":25},
    {"startup_id":"startup-005","fund_id":"fund-001","ticket_usd":700_000,"target_ownership_pct":15.42,"dilution_per_round_pct":20,"expected_exit_multiple":9,"expected_exit_years":6,"follow_on_pct":25},
]

VALUATION_ANALYSES = [
    {
        "startup_id": "startup-001",
        "round_id": "r-002",
        "pre_money_val": 6_000_000,
        "arr_at_time": 210_000,
        "multiple_paid": 28.6,
        "segment": "Fintech Neobank Seed LATAM",
        "market_p25": 9, "market_p50": 13, "market_p75": 18,
        "premium_pct": 120,
        "verdict": "premium_justified",
        "justification": "NRR 118% + crecimiento 233% YoY + LTV:CAC 7x. Todos por encima del P75 del segmento."
    },
    {
        "startup_id": "startup-002",
        "round_id": "r-004",
        "pre_money_val": 22_000_000,
        "arr_at_time": 1_800_000,
        "multiple_paid": 12.2,
        "segment": "LogTech Series A LATAM",
        "market_p25": 4, "market_p50": 6, "market_p75": 9,
        "premium_pct": 103,
        "verdict": "premium_justified",
        "justification": "NRR 124% best-in-class + burn multiple 1.4x excepcional + expansion MX→CO probada."
    },
    {
        "startup_id": "startup-004",
        "round_id": "r-007",
        "pre_money_val": 5_500_000,
        "arr_at_time": 300_000,
        "multiple_paid": 18.3,
        "segment": "Fintech Digital Lending Seed LATAM",
        "market_p25": 9, "market_p50": 13, "market_p75": 18,
        "premium_pct": 41,
        "verdict": "within_range",
        "justification": "Crecimiento 517% YoY excepcional pero NPL 4.2% en el límite aceptable. Múltiplo en P75."
    },
    {
        "startup_id": "startup-005",
        "round_id": "r-009",
        "pre_money_val": 7_000_000,
        "arr_at_time": 280_000,
        "multiple_paid": 25.0,
        "segment": "AgriTech SaaS Seed LATAM",
        "market_p25": 6, "market_p50": 9, "market_p75": 14,
        "premium_pct": 178,
        "verdict": "premium_justified",
        "justification": "Nicho con muy poca competencia VC-backed en Colombia. NRR 112% + LTV:CAC 6.5x. Moat de hardware IoT."
    },
]

FUND_SCENARIO_BASE = {
    "fund_id": "fund-001",
    "scenario_type": "base",
    "assumptions": {
        "total_investments": 5,
        "avg_ticket_usd": 730_000,
        "total_deployed_usd": 3_650_000,
        "winners_pct": 20,
        "avg_winner_multiple": 15,
        "avg_loss_rate_pct": 40,
        "fund_life_years": 10,
        "mgmt_fee_pct": 2.0,
        "carry_pct": 20,
    },
    "moic_p25": 1.8, "moic_p50": 2.6, "moic_p75": 3.8,
    "irr_p25": 14.0, "irr_p50": 19.0, "irr_p75": 26.0,
    "dpi_projected": 0.0,
    "tvpi_projected": 1.4,
}

FUND_SCENARIO_HIGH = {
    "fund_id": "fund-001",
    "scenario_type": "high",
    "assumptions": {
        "winners_pct": 40,
        "avg_winner_multiple": 22,
        "avg_loss_rate_pct": 25,
    },
    "moic_p25": 3.2, "moic_p50": 4.8, "moic_p75": 7.2,
    "irr_p25": 22.0, "irr_p50": 31.0, "irr_p75": 42.0,
    "dpi_projected": 0.0,
    "tvpi_projected": 2.1,
}

FUND_SCENARIO_DOWNSIDE = {
    "fund_id": "fund-001",
    "scenario_type": "downside",
    "assumptions": {
        "winners_pct": 10,
        "avg_winner_multiple": 8,
        "avg_loss_rate_pct": 60,
    },
    "moic_p25": 0.8, "moic_p50": 1.1, "moic_p75": 1.6,
    "irr_p25": -4.0, "irr_p50": 2.0, "irr_p75": 9.0,
    "dpi_projected": 0.0,
    "tvpi_projected": 0.9,
}

if __name__ == "__main__":
    total_records = (
        1 +  # fund
        len(STARTUPS) +
        len(FOUNDERS) +
        len(FUNDING_ROUNDS) +
        len(METRIC_SNAPSHOTS) +
        len(INVESTMENTS) +
        len(STUDIO_COMPANIES) +
        len(DEAL_ASSUMPTIONS) +
        len(VALUATION_ANALYSES) +
        3  # scenarios
    )
    print(f"AIDA Venture OS — Seed Data Summary")
    print(f"======================================")
    print(f"Fund:               1")
    print(f"Startups:           {len(STARTUPS)}")
    print(f"Founders:           {len(FOUNDERS)}")
    print(f"Funding rounds:     {len(FUNDING_ROUNDS)}")
    print(f"Metric snapshots:   {len(METRIC_SNAPSHOTS)}")
    print(f"Investments:        {len(INVESTMENTS)}")
    print(f"Studio companies:   {len(STUDIO_COMPANIES)}")
    print(f"Deal assumptions:   {len(DEAL_ASSUMPTIONS)}")
    print(f"Valuation analyses: {len(VALUATION_ANALYSES)}")
    print(f"Fund scenarios:     3 (base / high / downside)")
    print(f"--------------------------------------")
    print(f"TOTAL RECORDS:      {total_records}")
