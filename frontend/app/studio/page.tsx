'use client'

import { useEffect, useState } from 'react'
import PageWrapper from '@/components/layout/PageWrapper'
import Card from '@/components/ui/Card'
import KPICard from '@/components/ui/KPICard'
import SectionTitle from '@/components/ui/SectionTitle'
import Table from '@/components/ui/Table'
import DonutChart from '@/components/charts/DonutChart'
import { getStudioSummary } from '@/lib/api'
import * as mockStudio from '@/lib/mock/studio'
import type { StudioSummary } from '@/lib/types'

const fmtUSD = (v: number) =>
  v >= 1_000_000 ? `$${(v / 1_000_000).toFixed(2)}M` : `$${(v / 1_000).toFixed(0)}K`

const phaseColors: Record<string, string> = {
  'MVP':          '#1A6FE8',
  'Validación':   '#F5A623',
  'Seed externo': '#22C55E',
  'Idea':         '#9CA3AF',
}

export default function StudioPage() {
  const [summary, setSummary] = useState<StudioSummary | null>(null)

  useEffect(() => {
    getStudioSummary().then(setSummary)
  }, [])

  const donutData = summary
    ? Object.entries(summary.companies_by_phase).map(([name, value]) => ({ name, value }))
    : []

  const donutColors = donutData.map((d) => phaseColors[d.name] ?? '#9CA3AF')

  const companyRows = mockStudio.companies.map((c) => [
    <span key="name" className="font-medium">{c.startup_name}</span>,
    <span
      key="phase"
      className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
      style={{
        background: `${phaseColors[c.phase] ?? '#9CA3AF'}18`,
        color: phaseColors[c.phase] ?? '#9CA3AF',
      }}
    >
      {c.phase}
    </span>,
    fmtUSD(c.build_cost_usd),
    c.graduation_date
      ? new Date(c.graduation_date).toLocaleDateString('es-CO', { year: 'numeric', month: 'short' })
      : '—',
  ])

  const alphaRows = mockStudio.alphaMetrics.map((a) => [
    a.startup_name,
    a.metric,
    String(a.studio_value),
    String(a.market_p50),
    <span
      key="delta"
      className={a.delta > 0 ? 'text-[#22C55E] font-semibold' : 'text-[#EF4444] font-semibold'}
    >
      {a.delta > 0 ? `+${a.delta}` : String(a.delta)}
    </span>,
  ])

  return (
    <PageWrapper>
      {/* KPIs */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard label="Empresas totales" value={String(summary?.total_companies ?? 5)} />
        <KPICard
          label="Graduation rate"
          value={`${summary?.graduation_rate_pct ?? 40}%`}
          trend="up"
        />
        <KPICard
          label="Build cost total"
          value={fmtUSD(summary?.total_build_cost_usd ?? 850000)}
        />
        <KPICard
          label="Build cost prom."
          value={fmtUSD(summary?.avg_build_cost_usd ?? 170000)}
          delta={-32}
          trend="up"
          deltaLabel="vs benchmark LATAM"
        />
      </div>

      {/* Phase chart + companies */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card>
          <SectionTitle title="Empresas por fase" className="mb-2" />
          <DonutChart data={donutData} height={220} colors={donutColors} />
        </Card>

        <Card className="lg:col-span-2" padding="sm">
          <SectionTitle title="Empresas del studio" className="mb-4 px-2" />
          <Table
            headers={['Empresa', 'Fase', 'Build cost', 'Graduación']}
            rows={companyRows}
          />
        </Card>
      </div>

      {/* Alpha metrics */}
      <Card padding="sm">
        <SectionTitle
          title="Alpha metrics"
          subtitle="Métricas donde el studio supera al mercado"
          className="mb-4 px-2"
        />
        <Table
          headers={['Empresa', 'Métrica', 'Studio', 'Mercado P50', 'Delta']}
          rows={alphaRows}
        />
      </Card>
    </PageWrapper>
  )
}
