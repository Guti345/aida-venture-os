'use client'

import { useState } from 'react'
import PageWrapper from '@/components/layout/PageWrapper'
import Card from '@/components/ui/Card'
import SectionTitle from '@/components/ui/SectionTitle'
import Table from '@/components/ui/Table'
import BarChart from '@/components/charts/BarChart'
import type { MarketSegment } from '@/lib/types'

const SECTORS = ['Fintech', 'LogTech', 'SaaS B2B', 'HealthTech', 'AgriTech', 'EdTech']

const fmtUSD = (v: number) =>
  v >= 1_000_000 ? `$${(v / 1_000_000).toFixed(1)}M` : `$${(v / 1_000).toFixed(0)}K`

const allSegments: MarketSegment[] = [
  { id: '1', sector: 'Fintech',    stage: 'Seed',      geography: 'Colombia', avg_arr_usd: 580000,  benchmark_count: 24 },
  { id: '2', sector: 'Fintech',    stage: 'Series A',  geography: 'Colombia', avg_arr_usd: 4200000, benchmark_count: 12 },
  { id: '3', sector: 'LogTech',    stage: 'Seed',      geography: 'LATAM',    avg_arr_usd: 420000,  benchmark_count: 18 },
  { id: '4', sector: 'LogTech',    stage: 'Series A',  geography: 'LATAM',    avg_arr_usd: 2800000, benchmark_count: 9  },
  { id: '5', sector: 'SaaS B2B',   stage: 'Pre-Seed',  geography: 'Colombia', avg_arr_usd: 85000,   benchmark_count: 31 },
  { id: '6', sector: 'HealthTech', stage: 'Seed',      geography: 'Colombia', avg_arr_usd: 310000,  benchmark_count: 15 },
  { id: '7', sector: 'AgriTech',   stage: 'Seed',      geography: 'Colombia', avg_arr_usd: 280000,  benchmark_count: 22 },
  { id: '8', sector: 'EdTech',     stage: 'Pre-Seed',  geography: 'Colombia', avg_arr_usd: 65000,   benchmark_count: 19 },
]

export default function MarketPage() {
  const [sectorFilter, setSectorFilter] = useState('')

  const segments = sectorFilter
    ? allSegments.filter((s) => s.sector === sectorFilter)
    : allSegments

  const tableRows = segments.map((s) => [
    <span key="sector" className="font-medium">{s.sector}</span>,
    s.stage,
    s.geography,
    fmtUSD(s.avg_arr_usd),
    String(s.benchmark_count),
  ])

  const chartData = segments.map((s) => ({
    name: `${s.sector} ${s.stage}`,
    value: s.avg_arr_usd,
  }))

  return (
    <PageWrapper>
      <SectionTitle
        title="Benchmarks de mercado"
        subtitle="ARR promedio por segmento — fuente: datos de mercado LATAM"
      />

      <Card padding="sm">
        <div className="flex items-center gap-3 px-2 py-1">
          <select
            value={sectorFilter}
            onChange={(e) => setSectorFilter(e.target.value)}
            className="border border-[#9CA3AF]/30 rounded px-3 py-1.5 text-sm bg-white focus:outline-none focus:border-[#1A6FE8]"
          >
            <option value="">Todos los sectores</option>
            {SECTORS.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          {sectorFilter && (
            <button
              onClick={() => setSectorFilter('')}
              className="text-sm text-[#9CA3AF] hover:text-[#EF4444] transition-colors"
            >
              Limpiar
            </button>
          )}
          <span className="ml-auto text-sm text-[#9CA3AF]">
            {segments.length} segmentos
          </span>
        </div>
      </Card>

      <Card>
        <SectionTitle title="ARR promedio por segmento" className="mb-4" />
        <BarChart data={chartData} height={240} valueFormatter={fmtUSD} />
      </Card>

      <Card padding="sm">
        <SectionTitle title="Segmentos" className="mb-4 px-2" />
        <Table
          headers={['Sector', 'Etapa', 'Geografía', 'ARR promedio', 'Benchmarks']}
          rows={tableRows}
        />
      </Card>
    </PageWrapper>
  )
}
