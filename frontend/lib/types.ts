export interface Startup {
  id: string
  name: string
  sector: string
  subsector?: string
  stage: string
  geography: string
  country: string
  status: 'active' | 'watchlist' | 'passed' | 'acquired'
  is_simulated: boolean
}

export interface MetricSnapshot {
  id: string
  startup_id: string
  metric_name: string
  value: number
  unit: string
  period_date: string
  source?: string
}

export interface FundData {
  id: string
  name: string
  vintage_year: number
  target_size_usd: number
  deployed_usd: number
  status: string
}

export interface Investment {
  id: string
  startup_name: string
  amount_usd: number
  stage_at_entry: string
  entry_date: string
  ownership_pct: number
}

export interface FundMetrics {
  moic_current: number
  irr_estimate_pct: number
  total_invested_usd: number
  portfolio_count: number
}

export interface ScenarioInput {
  scenario_label: string
  pct_winners?: number
  winner_multiple?: number
  n_iterations?: number
}

export interface ScenarioResult {
  label: string
  moic_p25: number
  moic_p50: number
  moic_p75: number
  irr_p25: number
  irr_p50: number
  irr_p75: number
  total_invested_usd: number
}

export interface DealOpportunity {
  id: string
  status: 'screening' | 'due_diligence' | 'term_sheet' | 'invested' | 'passed' | 'archived'
  startup_name: string
  sourcing_channel_name: string
  identified_at: string
  avg_thesis_score: number
  days_in_pipeline?: number
}

export interface SourcingChannel {
  id: string
  name: string
  channel_type: string
  is_active: boolean
  deals_count?: number
}

export interface StudioCompany {
  id: string
  startup_name: string
  phase: string
  build_cost_usd: number
  graduation_date?: string
}

export interface StudioSummary {
  total_companies: number
  graduation_rate_pct: number
  total_build_cost_usd: number
  avg_build_cost_usd: number
  companies_by_phase: Record<string, number>
}

export interface LPReportSummary {
  fund_name: string
  report_date: string
  total_invested_usd: number
  portfolio_companies: number
  fund_moic_current: number
  fund_irr_estimate_pct: number
  narrative_summary: string
}

export interface PortfolioSnapshotItem {
  startup_name: string
  sector: string
  stage: string
  arr_usd?: number
  mrr_usd?: number
  nrr_pct?: number
  burn_usd?: number
  runway_months?: number
}

export interface MarketSegment {
  id: string
  sector: string
  stage: string
  geography: string
  avg_arr_usd: number
  benchmark_count: number
}

export interface ChartDataPoint {
  name: string
  value: number
  [key: string]: string | number
}
