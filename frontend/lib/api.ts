import type {
  Startup,
  MetricSnapshot,
  FundData,
  Investment,
  FundMetrics,
  ScenarioInput,
  ScenarioResult,
  DealOpportunity,
  SourcingChannel,
  StudioSummary,
  LPReportSummary,
  PortfolioSnapshotItem,
  MarketSegment,
} from './types'
import * as mockPortfolio from './mock/portfolio'
import * as mockFund from './mock/fund'
import * as mockStudio from './mock/studio'
import * as mockDeals from './mock/deals'
import * as mockReports from './mock/reports'

const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'
const DEMO_TOKEN = process.env.NEXT_PUBLIC_DEMO_TOKEN ?? ''

function authHeaders(): HeadersInit {
  return DEMO_TOKEN ? { Authorization: `Bearer ${DEMO_TOKEN}` } : {}
}

async function get<T>(path: string, params?: Record<string, string>): Promise<T> {
  const url = new URL(`${BASE}${path}`)
  if (params) {
    Object.entries(params).forEach(([k, v]) => v && url.searchParams.set(k, v))
  }
  const res = await fetch(url.toString(), {
    headers: { ...authHeaders() },
    cache: 'no-store',
  })
  if (!res.ok) throw new Error(`API error ${res.status}`)
  return res.json() as Promise<T>
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(body),
    cache: 'no-store',
  })
  if (!res.ok) throw new Error(`API error ${res.status}`)
  return res.json() as Promise<T>
}

export interface StartupFilters {
  name?: string
  sector?: string
  stage?: string
  country?: string
}

export async function getStartups(filters?: StartupFilters): Promise<Startup[]> {
  try {
    return await get<Startup[]>('/startups', {
      name: filters?.name ?? '',
      sector: filters?.sector ?? '',
      stage: filters?.stage ?? '',
      country: filters?.country ?? '',
    })
  } catch {
    let results = [...mockPortfolio.startups]
    if (filters?.sector) results = results.filter((s) => s.sector === filters.sector)
    if (filters?.stage)  results = results.filter((s) => s.stage === filters.stage)
    if (filters?.country) results = results.filter((s) => s.country === filters.country)
    if (filters?.name)   results = results.filter((s) => s.name.toLowerCase().includes(filters.name!.toLowerCase()))
    return results
  }
}

export async function getStartup(name: string): Promise<Startup | null> {
  try {
    return await get<Startup>(`/startups/${encodeURIComponent(name)}`)
  } catch {
    return mockPortfolio.startups.find((s) => s.name.toLowerCase() === name.toLowerCase()) ?? null
  }
}

export async function getMetricsLatest(name: string): Promise<Record<string, MetricSnapshot>> {
  try {
    return await get<Record<string, MetricSnapshot>>(`/startups/${encodeURIComponent(name)}/metrics/latest`)
  } catch {
    const snapshots = mockPortfolio.metricsMap[name] ?? []
    const result: Record<string, MetricSnapshot> = {}
    for (const s of snapshots) result[s.metric_name] = s
    return result
  }
}

export async function getMetricsHistory(name: string): Promise<MetricSnapshot[]> {
  try {
    return await get<MetricSnapshot[]>(`/startups/${encodeURIComponent(name)}/metrics`)
  } catch {
    return mockPortfolio.metricsMap[name] ?? []
  }
}

export async function getFund(): Promise<FundData> {
  try {
    return await get<FundData>('/fund')
  } catch {
    return mockFund.fund
  }
}

export async function getFundInvestments(): Promise<Investment[]> {
  try {
    return await get<Investment[]>('/fund/investments')
  } catch {
    return mockFund.investments
  }
}

export async function getFundMetrics(): Promise<FundMetrics> {
  try {
    return await get<FundMetrics>('/fund/metrics')
  } catch {
    return mockFund.metrics
  }
}

export async function getFundScenarios(): Promise<ScenarioResult[]> {
  try {
    return await get<ScenarioResult[]>('/fund/scenarios')
  } catch {
    return mockFund.savedScenarios
  }
}

export async function simulateFund(input: ScenarioInput): Promise<ScenarioResult> {
  try {
    return await post<ScenarioResult>('/fund/simulate', input)
  } catch {
    const preset = mockFund.savedScenarios.find((s) => s.label === input.scenario_label)
    return preset ?? mockFund.savedScenarios[1]
  }
}

export async function getStudioSummary(): Promise<StudioSummary> {
  try {
    return await get<StudioSummary>('/studio/summary')
  } catch {
    return mockStudio.summary
  }
}

export async function getDeals(status?: string): Promise<DealOpportunity[]> {
  try {
    return await get<DealOpportunity[]>('/deals', status ? { status } : undefined)
  } catch {
    if (status) return mockDeals.deals.filter((d) => d.status === status)
    return mockDeals.deals
  }
}

export async function getSourcingChannels(): Promise<SourcingChannel[]> {
  try {
    return await get<SourcingChannel[]>('/sourcing/channels')
  } catch {
    return mockDeals.channels
  }
}

export async function getLPReport(): Promise<LPReportSummary> {
  try {
    return await get<LPReportSummary>('/reports/lp-summary')
  } catch {
    return mockReports.lpReport
  }
}

export async function getPortfolioSnapshot(): Promise<PortfolioSnapshotItem[]> {
  try {
    return await get<PortfolioSnapshotItem[]>('/reports/portfolio-snapshot')
  } catch {
    return mockReports.portfolioSnapshot
  }
}

export async function getMarketSegments(): Promise<MarketSegment[]> {
  try {
    return await get<MarketSegment[]>('/market/segments')
  } catch {
    return [
      { id: '1', sector: 'Fintech',    stage: 'Seed',      geography: 'Colombia', avg_arr_usd: 580000,  benchmark_count: 24 },
      { id: '2', sector: 'Fintech',    stage: 'Series A',  geography: 'Colombia', avg_arr_usd: 4200000, benchmark_count: 12 },
      { id: '3', sector: 'LogTech',    stage: 'Seed',      geography: 'LATAM',    avg_arr_usd: 420000,  benchmark_count: 18 },
      { id: '4', sector: 'LogTech',    stage: 'Series A',  geography: 'LATAM',    avg_arr_usd: 2800000, benchmark_count: 9  },
      { id: '5', sector: 'SaaS B2B',   stage: 'Pre-Seed',  geography: 'Colombia', avg_arr_usd: 85000,   benchmark_count: 31 },
      { id: '6', sector: 'HealthTech', stage: 'Seed',      geography: 'Colombia', avg_arr_usd: 310000,  benchmark_count: 15 },
      { id: '7', sector: 'AgriTech',   stage: 'Seed',      geography: 'Colombia', avg_arr_usd: 280000,  benchmark_count: 22 },
      { id: '8', sector: 'EdTech',     stage: 'Pre-Seed',  geography: 'Colombia', avg_arr_usd: 65000,   benchmark_count: 19 },
    ]
  }
}
