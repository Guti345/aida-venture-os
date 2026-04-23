'use client'

import { useRouter } from 'next/navigation'
import PageWrapper from '@/components/layout/PageWrapper'
import KPICard from '@/components/ui/KPICard'
import Card from '@/components/ui/Card'
import SectionTitle from '@/components/ui/SectionTitle'
import Table from '@/components/ui/Table'
import Badge from '@/components/ui/Badge'
import BarChart from '@/components/charts/BarChart'
import DonutChart from '@/components/charts/DonutChart'
import { startups } from '@/lib/mock/portfolio'
import * as mockStudio from '@/lib/mock/studio'
import * as mockDeals from '@/lib/mock/deals'

const fmt = (v: number) =>
  v >= 1_000_000 ? `$${(v / 1_000_000).toFixed(2)}M` : `$${(v / 1_000).toFixed(0)}K`

const dealBarData = Object.entries(mockDeals.dealsByStatus).map(([name, value]) => ({
  name: name.replace('_', ' '),
  value,
}))

const studioDonutData = Object.entries(mockStudio.summary.companies_by_phase).map(
  ([name, value]) => ({ name, value })
)

export default function DashboardPage() {
  const router = useRouter()

  const tableRows = startups.slice(0, 8).map((s) => [
    <span key="name" className="font-medium text-[#0A0B0E]">{s.name}</span>,
    s.sector,
    s.stage,
    s.country,
    <Badge key="status" value={s.status} />,
  ])

  return (
    <PageWrapper>
      {/* KPI row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          label="Total Invertido"
          value="$3.15M"
          delta={12}
          trend="up"
          deltaLabel="vs Q4 2024"
        />
        <KPICard
          label="Portafolio Activo"
          value="10"
          unit="startups"
          delta={2}
          trend="up"
          deltaLabel="nuevas"
        />
        <KPICard
          label="MOIC Estimado"
          value="2.83x"
          delta={0.15}
          trend="up"
          deltaLabel="vs Q4 2024"
        />
        <KPICard
          label="Deals en Pipeline"
          value="8"
          delta={3}
          trend="up"
          deltaLabel="este mes"
        />
      </div>

      {/* Portfolio table */}
      <Card padding="sm">
        <div className="flex items-center justify-between mb-4 px-2">
          <SectionTitle title="Portafolio" subtitle="Startups activas y en watchlist" />
          <button
            onClick={() => router.push('/portfolio')}
            className="text-sm text-[#1A6FE8] hover:underline"
          >
            Ver todos →
          </button>
        </div>
        <Table
          headers={['Nombre', 'Sector', 'Etapa', 'País', 'Estado']}
          rows={tableRows}
          onRowClick={(i) => router.push(`/portfolio/${startups[i]?.name}`)}
        />
      </Card>

      {/* Studio + Pipeline */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <SectionTitle
            title="Venture Studio"
            subtitle="Empresas por fase de desarrollo"
            className="mb-4"
          />
          <div className="grid grid-cols-3 gap-3 mb-4">
            <div className="text-center">
              <p className="text-2xl font-semibold text-[#0A0B0E]">
                {mockStudio.summary.total_companies}
              </p>
              <p className="text-xs text-[#9CA3AF]">Empresas</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-semibold text-[#22C55E]">
                {mockStudio.summary.graduation_rate_pct}%
              </p>
              <p className="text-xs text-[#9CA3AF]">Graduation rate</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-semibold text-[#0A0B0E]">
                {fmt(mockStudio.summary.avg_build_cost_usd)}
              </p>
              <p className="text-xs text-[#9CA3AF]">Build cost prom.</p>
            </div>
          </div>
          <DonutChart data={studioDonutData} height={180} />
        </Card>

        <Card>
          <SectionTitle
            title="Deal Pipeline"
            subtitle="Deals activos por estado"
            className="mb-4"
          />
          <BarChart
            data={dealBarData}
            height={220}
            valueFormatter={(v) => String(v)}
          />
        </Card>
      </div>
    </PageWrapper>
  )
}
