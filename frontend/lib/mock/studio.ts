import type { StudioSummary, StudioCompany } from '../types'

export const summary: StudioSummary = {
  total_companies: 5,
  graduation_rate_pct: 40,
  total_build_cost_usd: 850000,
  avg_build_cost_usd: 170000,
  companies_by_phase: {
    MVP: 2,
    Validación: 2,
    'Seed externo': 1,
  },
}

export const companies: StudioCompany[] = [
  { id: 'studio-001', startup_name: 'EduStack',  phase: 'MVP',          build_cost_usd: 120000 },
  { id: 'studio-002', startup_name: 'LegalBot',  phase: 'Validación',   build_cost_usd: 95000  },
  { id: 'studio-003', startup_name: 'FleetOS',   phase: 'Seed externo', build_cost_usd: 210000, graduation_date: '2024-06-01' },
  { id: 'studio-004', startup_name: 'InsureX',   phase: 'MVP',          build_cost_usd: 85000  },
  { id: 'studio-005', startup_name: 'TaxFlow',   phase: 'Validación',   build_cost_usd: 140000 },
]

export const alphaMetrics = [
  { startup_name: 'FleetOS',  metric: 'NRR',           studio_value: 115, market_p50: 108, delta: 7  },
  { startup_name: 'FleetOS',  metric: 'Burn Multiple',  studio_value: 0.8, market_p50: 1.2, delta: -0.4 },
  { startup_name: 'TaxFlow',  metric: 'MoM Growth',     studio_value: 18,  market_p50: 12,  delta: 6  },
  { startup_name: 'EduStack', metric: 'CAC Payback',    studio_value: 4,   market_p50: 6,   delta: -2 },
]
