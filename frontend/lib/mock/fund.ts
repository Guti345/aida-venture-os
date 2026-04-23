import type { FundData, Investment, FundMetrics, ScenarioResult } from '../types'

export const fund: FundData = {
  id: 'fund-0001-0001-0001-000000000001',
  name: 'AIDA Ventures Fund I',
  vintage_year: 2023,
  target_size_usd: 10000000,
  deployed_usd: 3150000,
  status: 'investing',
}

export const investments: Investment[] = [
  { id: 'inv-001', startup_name: 'FinStack',  amount_usd: 300000,  stage_at_entry: 'Seed',     entry_date: '2023-08-15', ownership_pct: 8.5  },
  { id: 'inv-002', startup_name: 'LogiFlow',  amount_usd: 750000,  stage_at_entry: 'Series A', entry_date: '2023-11-20', ownership_pct: 5.2  },
  { id: 'inv-003', startup_name: 'MediSync',  amount_usd: 150000,  stage_at_entry: 'Pre-Seed', entry_date: '2024-01-10', ownership_pct: 12.0 },
  { id: 'inv-004', startup_name: 'CreditIA',  amount_usd: 400000,  stage_at_entry: 'Seed',     entry_date: '2024-02-28', ownership_pct: 9.0  },
  { id: 'inv-005', startup_name: 'AgriSense', amount_usd: 250000,  stage_at_entry: 'Seed',     entry_date: '2024-04-05', ownership_pct: 7.5  },
  { id: 'inv-006', startup_name: 'EduStack',  amount_usd: 200000,  stage_at_entry: 'Pre-Seed', entry_date: '2024-05-12', ownership_pct: 15.0 },
  { id: 'inv-007', startup_name: 'LegalBot',  amount_usd: 100000,  stage_at_entry: 'Pre-Seed', entry_date: '2024-07-01', ownership_pct: 10.0 },
  { id: 'inv-008', startup_name: 'FleetOS',   amount_usd: 350000,  stage_at_entry: 'Seed',     entry_date: '2024-08-20', ownership_pct: 8.0  },
  { id: 'inv-009', startup_name: 'TaxFlow',   amount_usd: 200000,  stage_at_entry: 'Pre-Seed', entry_date: '2024-10-15', ownership_pct: 11.0 },
]

export const metrics: FundMetrics = {
  moic_current: 2.83,
  irr_estimate_pct: 22.4,
  total_invested_usd: 3150000,
  portfolio_count: 10,
}

export const savedScenarios: ScenarioResult[] = [
  {
    label: 'conservador',
    moic_p25: 1.1,
    moic_p50: 1.8,
    moic_p75: 2.4,
    irr_p25: 6.2,
    irr_p50: 14.8,
    irr_p75: 21.3,
    total_invested_usd: 3150000,
  },
  {
    label: 'base',
    moic_p25: 1.6,
    moic_p50: 2.83,
    moic_p75: 4.1,
    irr_p25: 12.4,
    irr_p50: 22.4,
    irr_p75: 34.1,
    total_invested_usd: 3150000,
  },
  {
    label: 'optimista',
    moic_p25: 2.8,
    moic_p50: 4.2,
    moic_p75: 6.5,
    irr_p25: 24.1,
    irr_p50: 35.2,
    irr_p75: 52.8,
    total_invested_usd: 3150000,
  },
]
