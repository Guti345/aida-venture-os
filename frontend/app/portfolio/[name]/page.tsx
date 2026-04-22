'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import PageWrapper from '@/components/layout/PageWrapper'
import Card from '@/components/ui/Card'
import KPICard from '@/components/ui/KPICard'
import Badge from '@/components/ui/Badge'
import SectionTitle from '@/components/ui/SectionTitle'
import LineChart from '@/components/charts/LineChart'
import { getStartup, getMetricsHistory } from '@/lib/api'
import * as mockPortfolio from '@/lib/mock/portfolio'
import type { Startup, MetricSnapshot } from '@/lib/types'
import { ArrowLeft } from 'lucide-react'

const fmtUSD = (v: number) =>
  v >= 1_000_000 ? `$${(v / 1_000_000).toFixed(2)}M` : `$${(v / 1_000).toFixed(0)}K`

function formatDate(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleDateString('es-CO', { month: 'short', year: '2-digit' })
}

export default function StartupDetailPage() {
  const params = useParams()
  const router = useRouter()
  const rawName = typeof params.name === 'string' ? params.name : ''
  const name = decodeURIComponent(rawName)

  const [startup, setStartup] = useState<Startup | null>(null)
  const [metrics, setMetrics] = useState<MetricSnapshot[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getStartup(name), getMetricsHistory(name)])
      .then(([s, m]) => {
        setStartup(s)
        setMetrics(m)
      })
      .finally(() => setLoading(false))
  }, [name])

  if (loading) {
    return (
      <PageWrapper>
        <div className="py-16 text-center text-[#9CA3AF] text-sm">Cargando...</div>
      </PageWrapper>
    )
  }

  if (!startup) {
    return (
      <PageWrapper>
        <div className="py-16 text-center text-[#9CA3AF] text-sm">Startup no encontrada.</div>
      </PageWrapper>
    )
  }

  const latest = mockPortfolio.latestMetrics[startup.name] ?? {}
  const arrHistory = metrics
    .filter((m) => m.metric_name === 'arr')
    .sort((a, b) => a.period_date.localeCompare(b.period_date))
    .map((m) => ({ date: formatDate(m.period_date), value: m.value }))

  const percentile = 65

  return (
    <PageWrapper>
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <button
            onClick={() => router.back()}
            className="flex items-center gap-1 text-sm text-[#9CA3AF] hover:text-[#0A0B0E] mb-3 transition-colors"
          >
            <ArrowLeft size={14} /> Volver
          </button>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-semibold text-[#0A0B0E]">{startup.name}</h1>
            <Badge value={startup.status} />
          </div>
          <p className="text-sm text-[#9CA3AF] mt-1">
            {startup.sector}
            {startup.subsector ? ` · ${startup.subsector}` : ''} · {startup.stage} · {startup.geography}
          </p>
        </div>
      </div>

      {/* KPI row */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <KPICard
          label="ARR"
          value={fmtUSD(latest.arr ?? 0)}
          trend={latest.arr > 200000 ? 'up' : 'neutral'}
        />
        <KPICard
          label="MRR"
          value={fmtUSD(latest.mrr ?? 0)}
          trend="up"
        />
        <KPICard
          label="NRR"
          value={`${latest.nrr ?? 0}%`}
          trend={latest.nrr >= 110 ? 'up' : latest.nrr < 100 ? 'down' : 'neutral'}
        />
        <KPICard
          label="Burn mensual"
          value={fmtUSD(latest.burn ?? 0)}
          trend={latest.burn > 50000 ? 'down' : 'neutral'}
        />
        <KPICard
          label="Runway"
          value={`${latest.runway ?? 0}`}
          unit="meses"
          trend={latest.runway >= 12 ? 'up' : 'down'}
        />
      </div>

      {/* ARR chart + percentile */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <SectionTitle title="ARR histórico" className="mb-4" />
          {arrHistory.length > 0 ? (
            <LineChart
              data={arrHistory}
              height={220}
              valueFormatter={fmtUSD}
            />
          ) : (
            <div className="py-8 text-center text-sm text-[#9CA3AF]">Sin datos históricos</div>
          )}
        </Card>

        <Card>
          <SectionTitle
            title="Percentil vs mercado"
            subtitle={`Segmento: ${startup.sector} · ${startup.stage}`}
            className="mb-6"
          />
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-[#9CA3AF]">Posición</span>
                <span className="font-semibold text-[#1A6FE8]">P{percentile}</span>
              </div>
              <div className="w-full h-3 bg-[#F5F7FA] rounded-full overflow-hidden border border-[#9CA3AF]/20">
                <div
                  className="h-full bg-[#1A6FE8] rounded-full transition-all"
                  style={{ width: `${percentile}%` }}
                />
              </div>
              <div className="flex justify-between text-xs text-[#9CA3AF] mt-1">
                <span>P0</span>
                <span>P50</span>
                <span>P100</span>
              </div>
            </div>
            <p className="text-xs text-[#9CA3AF] leading-relaxed">
              Esta startup supera al {percentile}% de empresas comparables en ARR dentro de su segmento de mercado.
            </p>
          </div>
        </Card>
      </div>
    </PageWrapper>
  )
}
