'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import PageWrapper from '@/components/layout/PageWrapper'
import Card from '@/components/ui/Card'
import SectionTitle from '@/components/ui/SectionTitle'
import Table from '@/components/ui/Table'
import Badge from '@/components/ui/Badge'
import { getStartups } from '@/lib/api'
import type { Startup } from '@/lib/types'

const SECTORS = ['Fintech', 'LogTech', 'HealthTech', 'AgriTech', 'EdTech', 'LegalTech', 'InsurTech']
const STAGES  = ['Pre-Seed', 'Seed', 'Series A', 'Series B']
const COUNTRIES = ['CO', 'MX', 'BR', 'AR']

export default function PortfolioPage() {
  const router = useRouter()
  const [startups, setStartups] = useState<Startup[]>([])
  const [sector, setSector]   = useState('')
  const [stage, setStage]     = useState('')
  const [country, setCountry] = useState('')
  const [search, setSearch]   = useState('')
  const [loading, setLoading] = useState(true)

  const load = useCallback(() => {
    setLoading(true)
    getStartups({ sector, stage, country, name: search })
      .then(setStartups)
      .finally(() => setLoading(false))
  }, [sector, stage, country, search])

  useEffect(() => {
    load()
  }, [load])

  const rows = startups.map((s) => [
    <span key="name" className="font-medium text-[#0A0B0E]">{s.name}</span>,
    s.sector,
    s.subsector ?? '—',
    s.stage,
    s.country,
    <Badge key="status" value={s.status} />,
    s.is_simulated ? (
      <span key="sim" className="text-xs text-[#9CA3AF]">Simulado</span>
    ) : (
      <span key="real" className="text-xs text-[#22C55E]">Real</span>
    ),
  ])

  return (
    <PageWrapper>
      <SectionTitle
        title="Portfolio Overview"
        subtitle={`${startups.length} startups — filtros aplicados`}
      />

      {/* Filters */}
      <Card padding="sm">
        <div className="flex flex-wrap gap-3 px-2 py-1">
          <input
            type="text"
            placeholder="Buscar por nombre..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border border-[#9CA3AF]/30 rounded px-3 py-1.5 text-sm focus:outline-none focus:border-[#1A6FE8] w-48"
          />
          <select
            value={sector}
            onChange={(e) => setSector(e.target.value)}
            className="border border-[#9CA3AF]/30 rounded px-3 py-1.5 text-sm focus:outline-none focus:border-[#1A6FE8] bg-white"
          >
            <option value="">Todos los sectores</option>
            {SECTORS.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          <select
            value={stage}
            onChange={(e) => setStage(e.target.value)}
            className="border border-[#9CA3AF]/30 rounded px-3 py-1.5 text-sm focus:outline-none focus:border-[#1A6FE8] bg-white"
          >
            <option value="">Todas las etapas</option>
            {STAGES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          <select
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            className="border border-[#9CA3AF]/30 rounded px-3 py-1.5 text-sm focus:outline-none focus:border-[#1A6FE8] bg-white"
          >
            <option value="">Todos los países</option>
            {COUNTRIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          {(sector || stage || country || search) && (
            <button
              onClick={() => { setSector(''); setStage(''); setCountry(''); setSearch('') }}
              className="text-sm text-[#9CA3AF] hover:text-[#EF4444] transition-colors"
            >
              Limpiar filtros
            </button>
          )}
        </div>
      </Card>

      {/* Table */}
      <Card padding="sm">
        {loading ? (
          <div className="py-12 text-center text-sm text-[#9CA3AF]">Cargando...</div>
        ) : (
          <Table
            headers={['Nombre', 'Sector', 'Subsector', 'Etapa', 'País', 'Estado', 'Datos']}
            rows={rows}
            onRowClick={(i) => router.push(`/portfolio/${encodeURIComponent(startups[i]?.name ?? '')}`)}
          />
        )}
      </Card>
    </PageWrapper>
  )
}
