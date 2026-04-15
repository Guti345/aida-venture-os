"""
AIDA Venture OS — Studio Seed Data
5 empresas simuladas del Venture Studio de AIDA para desarrollo del software.
Reemplazar con datos reales cuando el studio comience operaciones.

Ejecutar: python studio_seed_data.py
"""

STUDIO_STARTUPS = [
    {
        "id": "studio-001",
        "name": "EduStack",
        "sector": "EdTech",
        "subsector": "SaaS B2B para instituciones educativas",
        "stage": "Pre-Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Bogotá",
        "founded_at": "2024-01-15",
        "studio_built": True,
        "website": "edustack.co",
        "description": (
            "SaaS de gestión académica y seguimiento de aprendizaje para colegios y universidades. "
            "Módulos: matrícula digital, seguimiento académico, comunicación padres-institución. "
            "Modelo: SaaS mensual por institución."
        ),
        "status": "active",
        "is_simulated": True
    },
    {
        "id": "studio-002",
        "name": "LegalBot",
        "sector": "LegalTech",
        "subsector": "AI para automatización legal",
        "stage": "Pre-Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Bogotá",
        "founded_at": "2024-03-01",
        "studio_built": True,
        "website": "legalbot.co",
        "description": (
            "Plataforma de automatización de documentos legales con IA para PYMEs colombianas. "
            "Contratos, poderes, derechos de petición. Sin abogado para casos estándar. "
            "Modelo: créditos por documento + suscripción empresarial."
        ),
        "status": "active",
        "is_simulated": True
    },
    {
        "id": "studio-003",
        "name": "FleetOS",
        "sector": "LogTech",
        "subsector": "Gestión de flotillas de transporte",
        "stage": "Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Medellín",
        "founded_at": "2023-04-01",
        "studio_built": True,
        "website": "fleeetos.co",
        "description": (
            "SaaS de gestión integral de flotillas para empresas de transporte terrestre de carga. "
            "GPS tracking, mantenimiento predictivo, gestión de conductores y documentación. "
            "Modelo: SaaS mensual por vehículo."
        ),
        "status": "active",
        "is_simulated": True
    },
    {
        "id": "studio-004",
        "name": "InsureX",
        "sector": "InsurTech",
        "subsector": "Seguros embebidos B2B2C",
        "stage": "Pre-Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Bogotá",
        "founded_at": "2024-06-01",
        "studio_built": True,
        "website": "insurex.co",
        "description": (
            "Infraestructura de seguros embebidos para plataformas digitales y fintechs. "
            "API-first para integrar microseguros en cualquier flujo de compra o préstamo. "
            "Modelo: comisión por prima + SaaS de plataforma."
        ),
        "status": "active",
        "is_simulated": True
    },
    {
        "id": "studio-005",
        "name": "TaxFlow",
        "sector": "Fintech",
        "subsector": "Contabilidad y tributaria para PYMEs",
        "stage": "Pre-Seed",
        "geography": "LATAM",
        "country": "CO",
        "city": "Cali",
        "founded_at": "2024-02-15",
        "studio_built": True,
        "website": "taxflow.co",
        "description": (
            "Plataforma de contabilidad automatizada y cumplimiento tributario para PYMEs colombianas. "
            "Integración directa con DIAN, facturación electrónica y declaraciones automáticas. "
            "Modelo: SaaS mensual por empresa + módulos premium."
        ),
        "status": "active",
        "is_simulated": True
    },
]

STUDIO_FOUNDERS = [
    # EduStack
    {"id":"sf-001","startup_id":"studio-001","name":"Laura Pedraza","role":"CEO","email":"l.pedraza@edustack.co","equity_pct":40.0,
     "background":"Magíster en Educación U. de los Andes. Ex directora académica Colegio San Carlos. 10 años en gestión educativa."},
    {"id":"sf-002","startup_id":"studio-001","name":"Ricardo Gómez","role":"CTO","email":"r.gomez@edustack.co","equity_pct":25.0,
     "background":"Ingeniero de software Uniandes. Ex Platzi (infrastructure team). Especialista en sistemas educativos digitales."},
    # LegalBot
    {"id":"sf-003","startup_id":"studio-002","name":"Camila Vargas","role":"CEO","email":"c.vargas@legalbot.co","equity_pct":42.0,
     "background":"Abogada U. Externado + LLM en Legal Tech. Ex asociada Brigard Urrutia. Especialista en derecho corporativo."},
    {"id":"sf-004","startup_id":"studio-002","name":"Mateo Suárez","role":"CTO","email":"m.suarez@legalbot.co","equity_pct":26.0,
     "background":"Ingeniero de sistemas U. Nacional. Ex Rappi (ML team). Especialista en NLP en español."},
    # FleetOS
    {"id":"sf-005","startup_id":"studio-003","name":"Hernán Ríos","role":"CEO","email":"h.rios@fleeetos.co","equity_pct":38.0,
     "background":"Ingeniero industrial U. de Medellín + MBA EAFIT. 8 años en operaciones de transporte de carga. Ex TCC Colombia."},
    {"id":"sf-006","startup_id":"studio-003","name":"Ana Lucía Mora","role":"CTO","email":"a.mora@fleeetos.co","equity_pct":24.0,
     "background":"Ingeniera de sistemas U. de Antioquia. Ex Coordinadora (tech team). Especialista en IoT y tracking vehicular."},
    # InsureX
    {"id":"sf-007","startup_id":"studio-004","name":"Sebastián López","role":"CEO","email":"s.lopez@insurex.co","equity_pct":43.0,
     "background":"Economista U. de los Andes + MSc Finance LSE. Ex actuario Sura. 7 años en estructuración de productos de seguro."},
    {"id":"sf-008","startup_id":"studio-004","name":"Valentina Cruz","role":"CTO","email":"v.cruz@insurex.co","equity_pct":27.0,
     "background":"Ingeniera de sistemas U. Javeriana. Ex Kushki (payments API). Especialista en infraestructura financiera y APIs."},
    # TaxFlow
    {"id":"sf-009","startup_id":"studio-005","name":"Jorge Castaño","role":"CEO","email":"j.castano@taxflow.co","equity_pct":41.0,
     "background":"Contador público U. del Valle + MSc Tributaria. Ex socio BDO Colombia. 12 años en consultoría tributaria para PYMEs."},
    {"id":"sf-010","startup_id":"studio-005","name":"Daniela Parra","role":"CTO","email":"d.parra@taxflow.co","equity_pct":25.0,
     "background":"Ingeniera de sistemas U. Icesi. Ex desarrolladora Siigo (ERP contable). Especialista en integración con DIAN."},
]

STUDIO_COMPANIES = [
    {
        "startup_id": "studio-001",
        "idea_date": "2023-11-01",
        "validation_date": "2024-01-10",
        "mvp_date": "2024-04-01",
        "pmf_date": None,
        "first_external_seed_date": None,
        "build_cost_usd": 75_000,
        "equity_retained_pct": 45.0,
        "studio_support_level": "full",
        "current_studio_phase": "mvp",
        "notes": "Buena tracción inicial con colegios privados en Bogotá. Piloto activo con 3 instituciones."
    },
    {
        "startup_id": "studio-002",
        "idea_date": "2024-01-15",
        "validation_date": "2024-03-01",
        "mvp_date": None,
        "pmf_date": None,
        "first_external_seed_date": None,
        "build_cost_usd": 45_000,
        "equity_retained_pct": 48.0,
        "studio_support_level": "full",
        "current_studio_phase": "validation",
        "notes": "Regulación compleja en LATAM. Pivotando de B2C a B2B para reducir fricción de adopción."
    },
    {
        "startup_id": "studio-003",
        "idea_date": "2023-01-15",
        "validation_date": "2023-04-01",
        "mvp_date": "2023-07-01",
        "pmf_date": "2024-01-01",
        "first_external_seed_date": "2024-08-01",
        "build_cost_usd": 180_000,
        "equity_retained_pct": 38.0,
        "studio_support_level": "full",
        "current_studio_phase": "series_a_prep",
        "notes": "Primera empresa del studio en alcanzar PMF. Referencia de modelo para el studio. Levantó Seed externo con AIDA como lead."
    },
    {
        "startup_id": "studio-004",
        "idea_date": "2024-04-01",
        "validation_date": None,
        "mvp_date": None,
        "pmf_date": None,
        "first_external_seed_date": None,
        "build_cost_usd": 20_000,
        "equity_retained_pct": 50.0,
        "studio_support_level": "full",
        "current_studio_phase": "idea",
        "notes": "En fase de validación de hipótesis de negocio. Conversaciones con 2 fintechs potenciales como primeros clientes B2B."
    },
    {
        "startup_id": "studio-005",
        "idea_date": "2023-12-01",
        "validation_date": "2024-02-15",
        "mvp_date": None,
        "pmf_date": None,
        "first_external_seed_date": None,
        "build_cost_usd": 55_000,
        "equity_retained_pct": 46.0,
        "studio_support_level": "full",
        "current_studio_phase": "validation",
        "notes": "Integración con DIAN más compleja de lo esperado. Ajustando roadmap técnico. 8 PYMEs en piloto pagando."
    },
]

STUDIO_MILESTONES = [
    # EduStack
    {"startup_id":"studio-001","milestone_type":"idea","target_date":"2023-11-01","actual_date":"2023-11-01","achieved":True},
    {"startup_id":"studio-001","milestone_type":"validation","target_date":"2024-01-01","actual_date":"2024-01-10","achieved":True},
    {"startup_id":"studio-001","milestone_type":"mvp","target_date":"2024-03-01","actual_date":"2024-04-01","achieved":True,"notes":"1 mes de retraso por integración con sistema de notas legacy"},
    {"startup_id":"studio-001","milestone_type":"first_revenue","target_date":"2024-05-01","actual_date":"2024-05-15","achieved":True},
    {"startup_id":"studio-001","milestone_type":"pmf","target_date":"2024-10-01","actual_date":None,"achieved":False},
    # LegalBot
    {"startup_id":"studio-002","milestone_type":"idea","target_date":"2024-01-15","actual_date":"2024-01-15","achieved":True},
    {"startup_id":"studio-002","milestone_type":"validation","target_date":"2024-03-01","actual_date":"2024-03-01","achieved":True},
    {"startup_id":"studio-002","milestone_type":"mvp","target_date":"2024-06-01","actual_date":None,"achieved":False,"notes":"Pivote a B2B retrasó el MVP 3 meses"},
    # FleetOS — empresa más madura del studio
    {"startup_id":"studio-003","milestone_type":"idea","target_date":"2023-01-15","actual_date":"2023-01-15","achieved":True},
    {"startup_id":"studio-003","milestone_type":"validation","target_date":"2023-04-01","actual_date":"2023-04-01","achieved":True},
    {"startup_id":"studio-003","milestone_type":"mvp","target_date":"2023-07-01","actual_date":"2023-07-01","achieved":True},
    {"startup_id":"studio-003","milestone_type":"first_revenue","target_date":"2023-08-01","actual_date":"2023-08-15","achieved":True},
    {"startup_id":"studio-003","milestone_type":"pmf","target_date":"2023-12-01","actual_date":"2024-01-01","achieved":True,"notes":"PMF validado con NRR > 110% y 15+ clientes pagando"},
    {"startup_id":"studio-003","milestone_type":"seed","target_date":"2024-06-01","actual_date":"2024-08-01","achieved":True,"notes":"Seed externo $600K liderado por AIDA con co-investor Latitud"},
    # InsureX
    {"startup_id":"studio-004","milestone_type":"idea","target_date":"2024-04-01","actual_date":"2024-04-01","achieved":True},
    {"startup_id":"studio-004","milestone_type":"validation","target_date":"2024-08-01","actual_date":None,"achieved":False,"notes":"En proceso. Conversaciones activas con 2 fintechs"},
    # TaxFlow
    {"startup_id":"studio-005","milestone_type":"idea","target_date":"2023-12-01","actual_date":"2023-12-01","achieved":True},
    {"startup_id":"studio-005","milestone_type":"validation","target_date":"2024-02-15","actual_date":"2024-02-15","achieved":True},
    {"startup_id":"studio-005","milestone_type":"mvp","target_date":"2024-05-01","actual_date":None,"achieved":False,"notes":"Retrasado por complejidad de API DIAN"},
]

STUDIO_BUILD_COSTS = [
    # EduStack
    {"startup_id":"studio-001","cost_type":"personnel","amount_usd":45_000,"period_date":"2024-04-01","notes":"Salarios equipo técnico 3 meses"},
    {"startup_id":"studio-001","cost_type":"tech","amount_usd":8_000,"period_date":"2024-04-01","notes":"Infraestructura cloud + herramientas"},
    {"startup_id":"studio-001","cost_type":"ops","amount_usd":12_000,"period_date":"2024-04-01","notes":"Legal, registro, coworking"},
    {"startup_id":"studio-001","cost_type":"marketing","amount_usd":10_000,"period_date":"2024-04-01","notes":"Validación con instituciones educativas"},
    # LegalBot
    {"startup_id":"studio-002","cost_type":"personnel","amount_usd":28_000,"period_date":"2024-03-01","notes":"Equipo técnico + legal advisor"},
    {"startup_id":"studio-002","cost_type":"tech","amount_usd":7_000,"period_date":"2024-03-01","notes":"APIs LLM + infraestructura"},
    {"startup_id":"studio-002","cost_type":"legal","amount_usd":10_000,"period_date":"2024-03-01","notes":"Validación regulatoria del modelo de negocio"},
    # FleetOS
    {"startup_id":"studio-003","cost_type":"personnel","amount_usd":110_000,"period_date":"2024-01-01","notes":"Equipo 12 meses"},
    {"startup_id":"studio-003","cost_type":"tech","amount_usd":25_000,"period_date":"2024-01-01","notes":"Plataforma IoT + backend"},
    {"startup_id":"studio-003","cost_type":"ops","amount_usd":20_000,"period_date":"2024-01-01","notes":"Ventas, legal, oficina"},
    {"startup_id":"studio-003","cost_type":"marketing","amount_usd":25_000,"period_date":"2024-01-01","notes":"Eventos de industria + demos"},
    # InsureX
    {"startup_id":"studio-004","cost_type":"personnel","amount_usd":14_000,"period_date":"2024-06-01","notes":"Equipo fundador 2 meses"},
    {"startup_id":"studio-004","cost_type":"legal","amount_usd":6_000,"period_date":"2024-06-01","notes":"Análisis regulatorio Supersociedades"},
    # TaxFlow
    {"startup_id":"studio-005","cost_type":"personnel","amount_usd":38_000,"period_date":"2024-02-15","notes":"Equipo técnico + contador senior 4 meses"},
    {"startup_id":"studio-005","cost_type":"tech","amount_usd":9_000,"period_date":"2024-02-15","notes":"Licencias, infraestructura, APIs DIAN"},
    {"startup_id":"studio-005","cost_type":"ops","amount_usd":8_000,"period_date":"2024-02-15","notes":"Legal, registro, herramientas"},
]

STUDIO_METRICS = [
    # EduStack — Pre-Seed, primeros ingresos
    {"startup_id":"studio-001","metric_name":"MRR","value":1_800,"unit":"USD","period_date":"2024-06-01"},
    {"startup_id":"studio-001","metric_name":"MRR","value":3_200,"unit":"USD","period_date":"2024-09-01"},
    {"startup_id":"studio-001","metric_name":"MRR","value":4_800,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-001","metric_name":"active_customers","value":12,"unit":"institutions","period_date":"2024-12-01"},
    {"startup_id":"studio-001","metric_name":"gross_margin_pct","value":82,"unit":"pct","period_date":"2024-12-01"},
    {"startup_id":"studio-001","metric_name":"burn_rate_monthly","value":18_000,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-001","metric_name":"runway_months","value":12,"unit":"months","period_date":"2024-12-01"},
    {"startup_id":"studio-001","metric_name":"NRR_pct","value":106,"unit":"pct","period_date":"2024-12-01"},
    # LegalBot — Pre-Seed, sin ingresos aún
    {"startup_id":"studio-002","metric_name":"MRR","value":0,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-002","metric_name":"active_customers","value":0,"unit":"companies","period_date":"2024-12-01"},
    {"startup_id":"studio-002","metric_name":"burn_rate_monthly","value":14_000,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-002","metric_name":"runway_months","value":8,"unit":"months","period_date":"2024-12-01"},
    {"startup_id":"studio-002","metric_name":"waitlist_signups","value":340,"unit":"users","period_date":"2024-12-01"},
    # FleetOS — Seed, empresa madura del studio
    {"startup_id":"studio-003","metric_name":"MRR","value":8_000,"unit":"USD","period_date":"2023-09-01"},
    {"startup_id":"studio-003","metric_name":"MRR","value":14_000,"unit":"USD","period_date":"2023-12-01"},
    {"startup_id":"studio-003","metric_name":"MRR","value":22_000,"unit":"USD","period_date":"2024-03-01"},
    {"startup_id":"studio-003","metric_name":"MRR","value":31_000,"unit":"USD","period_date":"2024-06-01"},
    {"startup_id":"studio-003","metric_name":"MRR","value":38_000,"unit":"USD","period_date":"2024-09-01"},
    {"startup_id":"studio-003","metric_name":"MRR","value":45_000,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"ARR","value":540_000,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"active_customers","value":62,"unit":"fleets","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"gross_margin_pct","value":74,"unit":"pct","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"burn_rate_monthly","value":65_000,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"burn_multiple","value":1.5,"unit":"ratio","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"NRR_pct","value":116,"unit":"pct","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"CAC","value":2_800,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"LTV","value":19_600,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"LTV_CAC_ratio","value":7.0,"unit":"ratio","period_date":"2024-12-01"},
    {"startup_id":"studio-003","metric_name":"headcount","value":14,"unit":"people","period_date":"2024-12-01"},
    # InsureX — Idea, sin métricas financieras
    {"startup_id":"studio-004","metric_name":"design_partners","value":2,"unit":"fintechs","period_date":"2024-12-01"},
    {"startup_id":"studio-004","metric_name":"burn_rate_monthly","value":9_000,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-004","metric_name":"runway_months","value":6,"unit":"months","period_date":"2024-12-01"},
    # TaxFlow — Validación, primeros pagantes
    {"startup_id":"studio-005","metric_name":"MRR","value":1_200,"unit":"USD","period_date":"2024-09-01"},
    {"startup_id":"studio-005","metric_name":"MRR","value":2_400,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-005","metric_name":"active_customers","value":8,"unit":"companies","period_date":"2024-12-01"},
    {"startup_id":"studio-005","metric_name":"gross_margin_pct","value":79,"unit":"pct","period_date":"2024-12-01"},
    {"startup_id":"studio-005","metric_name":"burn_rate_monthly","value":16_000,"unit":"USD","period_date":"2024-12-01"},
    {"startup_id":"studio-005","metric_name":"runway_months","value":10,"unit":"months","period_date":"2024-12-01"},
    {"startup_id":"studio-005","metric_name":"NRR_pct","value":111,"unit":"pct","period_date":"2024-12-01"},
]

STUDIO_ALPHA_BENCHMARKS = {
    "series_a_graduation_rate_studio": 40.0,
    "series_a_graduation_rate_market_latam": 7.5,
    "avg_months_idea_to_pmf_studio": 18,
    "avg_months_idea_to_pmf_market": 30,
    "avg_build_cost_usd": 75_000,
    "avg_external_seed_valuation": 3_500_000,
    "implied_moic_on_build_cost": 46.7,
    "survival_rate_year_2_studio": 80.0,
    "survival_rate_year_2_market": 45.0,
}

if __name__ == "__main__":
    total = (
        len(STUDIO_STARTUPS) +
        len(STUDIO_FOUNDERS) +
        len(STUDIO_COMPANIES) +
        len(STUDIO_MILESTONES) +
        len(STUDIO_BUILD_COSTS) +
        len(STUDIO_METRICS) +
        1
    )
    print(f"AIDA Venture OS — Studio Seed Data Summary")
    print(f"===========================================")
    print(f"Studio startups:    {len(STUDIO_STARTUPS)}")
    print(f"Studio founders:    {len(STUDIO_FOUNDERS)}")
    print(f"Studio companies:   {len(STUDIO_COMPANIES)}")
    print(f"Studio milestones:  {len(STUDIO_MILESTONES)}")
    print(f"Build costs:        {len(STUDIO_BUILD_COSTS)}")
    print(f"Metric snapshots:   {len(STUDIO_METRICS)}")
    print(f"Alpha benchmarks:   1 (dict)")
    print(f"-------------------------------------------")
    print(f"TOTAL RECORDS:      {total}")
