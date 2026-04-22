'use client'

import { useState, useEffect, useCallback } from 'react'
import PageWrapper from '@/components/layout/PageWrapper'
import Card from '@/components/ui/Card'
import SectionTitle from '@/components/ui/SectionTitle'
import Table from '@/components/ui/Table'
import Badge from '@/components/ui/Badge'
import BarChart from '@/components/charts/BarChart'
import { getDeals, getSourcingChannels } from '@/lib/api'
import * as mockDeals from '@/lib/mock/deals'
import type { DealOpportunity, SourcingChannel } from '@/lib/types'

const STATUSES = ['screening', 'due_diligence', 'term_sheet', 'invested', 'passed', 'archived']

const dealBarData = Object.entries(mockDeals.dealsByStatus).map(([name, value]) => ({
  name: name.replace('_', ' '),
  value,
}))

export default function DealsPage() {
  const [deals, setDeals]     = useState<DealOpportunity[]>([])
  const [channels, setChannels] = useState<SourcingChannel[]>([])
  const [status, setStatus]   = useState('')
  const [loading, setLoading] = useState(true)

  const load = useCallback(() => {
    setLoading(true)
    Promise.all([getDeals(status || undefined), getSourcingChannels()])
      .then(([d, ch]) => { setDeals(d); setChannels(ch) })
      .finally(() => setLoading(false))
  }, [status])

  useEffect(() => { load() }, [load])

  const scoreColor = (score: number) =>
    score >= 75 ? 'text-[#22C55E]' : score >= 55 ? 'text-[#F5A623]' : 'text-[#EF4444]'

  const dealRows = deals.map((d) => [
    <span key="name" className="font-medium">{d.startup_name}</span>,
    <Badge key="status" value={d.status} />,
    d.sourcing_channel_name,
    new Date(d.identified_at).toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: 'numeric' }),
    d.days_in_pipeline !== undefined && d.days_in_pipeline > 0
      ? `${d.days_in_pipeline}d`
      : '—',
    <span key="score" className={`font-semibold ${scoreColor(d.avg_thesis_score)}`}>
      {d.avg_thesis_score}
    </span>,
  ])

  const channelRows = channels.map((ch) => [
    ch.name,
    ch.channel_type,
    <span
      key="active"
      className={ch.is_active ? 'text-[#22C55E] text-sm' : 'text-[#9CA3AF] text-sm'}
    >
      {ch.is_active ? 'Activo' : 'Inactivo'}
    </span>,
    String(ch.deals_count ?? 0),
  ])

  return (
    <PageWrapper>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(mockDeals.dealsByStatus).map(([key, val]) => (
          <div key={key} className="bg-white rounded-lg border border-[#9CA3AF]/20 p-4 text-center">
            <p className="text-2xl font-semibold text-[#0A0B0E]">{val}</p>
            <p className="text-xs text-[#9CA3AF] capitalize mt-1">{key.replace('_', ' ')}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2" padding="sm">
          <div className="flex items-center justify-between mb-4 px-2">
            <SectionTitle title="Pipeline de deals" />
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="border border-[#9CA3AF]/30 rounded px-3 py-1.5 text-sm bg-white focus:outline-none focus:border-[#1A6FE8]"
            >
              <option value="">Todos los estados</option>
              {STATUSES.map((s) => (
                <option key={s} value={s}>{s.replace('_', ' ')}</option>
              ))}
            </select>
          </div>
          {loading ? (
            <div className="py-8 text-center text-sm text-[#9CA3AF]">Cargando...</div>
          ) : (
            <Table
              headers={['Startup', 'Estado', 'Canal', 'Identificado', 'En pipeline', 'Thesis score']}
              rows={dealRows}
            />
          )}
        </Card>

        <Card>
          <SectionTitle title="Por estado" className="mb-4" />
          <BarChart data={dealBarData} height={200} valueFormatter={(v) => String(v)} />
        </Card>
      </div>

      {/* Sourcing channels */}
      <Card padding="sm">
        <SectionTitle
          title="Canales de sourcing"
          subtitle="Canales activos y deals asociados"
          className="mb-4 px-2"
        />
        <Table
          headers={['Canal', 'Tipo', 'Estado', 'Deals']}
          rows={channelRows}
        />
      </Card>
    </PageWrapper>
  )
}
