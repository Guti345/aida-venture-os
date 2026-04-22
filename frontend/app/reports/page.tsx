'use client'

import { useEffect, useState } from 'react'
import PageWrapper from '@/components/layout/PageWrapper'
import Card from '@/components/ui/Card'
import KPICard from '@/components/ui/KPICard'
import SectionTitle from '@/components/ui/SectionTitle'
import Table from '@/components/ui/Table'
import { getLPReport, getPortfolioSnapshot } from '@/lib/api'
import type { LPReportSummary, PortfolioSnapshotItem } from '@/lib/types'
import { FileText } from 'lucide-react'

const fmtUSD = (v?: number) => {
  if (v === undefined || v === null) return '—'
  return v >= 1_000_000 ? `$${(v / 1_000_000).toFixed(2)}M` : `$${(v / 1_000).toFixed(0)}K`
}

const runwayColor = (months?: number) => {
  if (!months) return 'text-[#9CA3AF]'
  if (months >= 12) return 'text-[#22C55E]'
  if (months >= 6)  return 'text-[#F5A623]'
  return 'text-[#EF4444]'
}

export default function ReportsPage() {
  const [report, setReport]     = useState<LPReportSummary | null>(null)
  const [snapshot, setSnapshot] = useState<PortfolioSnapshotItem[]>([])
  const [loading, setLoading]   = useState(true)

  useEffect(() => {
    Promise.all([getLPReport(), getPortfolioSnapshot()])
      .then(([r, s]) => { setReport(r); setSnapshot(s) })
      .finally(() => setLoading(false))
  }, [])

  const snapshotRows = snapshot.map((s) => [
    <span key="name" className="font-medium">{s.startup_name}</span>,
    s.sector,
    s.stage,
    fmtUSD(s.arr_usd),
    fmtUSD(s.mrr_usd),
    s.nrr_pct !== undefined ? `${s.nrr_pct}%` : '—',
    fmtUSD(s.burn_usd),
    s.runway_months !== undefined ? (
      <span key="runway" className={`font-semibold ${runwayColor(s.runway_months)}`}>
        {s.runway_months}m
      </span>
    ) : '—',
  ])

  return (
    <PageWrapper>
      {loading ? (
        <div className="py-16 text-center text-sm text-[#9CA3AF]">Cargando...</div>
      ) : (
        <>
          {/* KPIs */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <KPICard label="Fondo" value={report?.fund_name?.split(' ').slice(-2).join(' ') ?? '—'} />
            <KPICard label="Total invertido" value={fmtUSD(report?.total_invested_usd)} />
            <KPICard
              label="MOIC actual"
              value={report ? `${report.fund_moic_current.toFixed(2)}x` : '—'}
              trend="up"
            />
            <KPICard
              label="IRR estimado"
              value={report ? `${report.fund_irr_estimate_pct.toFixed(1)}%` : '—'}
              trend="up"
            />
          </div>

          {/* LP Summary narrative */}
          <Card>
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-[#1A6FE8]/10 flex items-center justify-center flex-shrink-0">
                <FileText size={18} className="text-[#1A6FE8]" />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <SectionTitle title="LP Report — Resumen ejecutivo" />
                  <span className="text-xs text-[#9CA3AF]">
                    {report?.report_date
                      ? new Date(report.report_date).toLocaleDateString('es-CO', {
                          year: 'numeric', month: 'long', day: 'numeric',
                        })
                      : ''}
                  </span>
                </div>
                <p className="text-sm text-[#0A0B0E] leading-relaxed">
                  {report?.narrative_summary}
                </p>
                <div className="mt-4 grid grid-cols-2 gap-4">
                  <div className="bg-[#F5F7FA] rounded-lg p-3">
                    <p className="text-xs text-[#9CA3AF]">Empresas en portafolio</p>
                    <p className="text-lg font-semibold text-[#0A0B0E] mt-0.5">
                      {report?.portfolio_companies}
                    </p>
                  </div>
                  <div className="bg-[#F5F7FA] rounded-lg p-3">
                    <p className="text-xs text-[#9CA3AF]">Fecha de reporte</p>
                    <p className="text-lg font-semibold text-[#0A0B0E] mt-0.5">
                      {report?.report_date
                        ? new Date(report.report_date).toLocaleDateString('es-CO', {
                            year: 'numeric', month: 'short',
                          })
                        : '—'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Portfolio snapshot */}
          <Card padding="sm">
            <SectionTitle
              title="Portfolio Snapshot"
              subtitle="Métricas operativas por startup — último período disponible"
              className="mb-4 px-2"
            />
            <Table
              headers={['Startup', 'Sector', 'Etapa', 'ARR', 'MRR', 'NRR', 'Burn', 'Runway']}
              rows={snapshotRows}
            />
          </Card>
        </>
      )}
    </PageWrapper>
  )
}
