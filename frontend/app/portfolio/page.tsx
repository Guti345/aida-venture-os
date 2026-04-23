'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import PageWrapper from '@/components/layout/PageWrapper'
import Card from '@/components/ui/Card'
import SectionTitle from '@/components/ui/SectionTitle'
import Table from '@/components/ui/Table'
import Badge from '@/components/ui/Badge'
import { startups as allStartups } from '@/lib/mock/portfolio'

const SECTORS = ['Fintech', 'LogTech', 'HealthTech', 'AgriTech', 'EdTech', 'LegalTech', 'InsurTech']
const STAGES  = ['Pre-Seed', 'Seed', 'Series A', 'Series B']
const COUNTRIES = ['CO', 'MX', 'BR', 'AR']

export default function PortfolioPage() {
  const router = useRouter()
  const [sector, setSector]   = useState('')
  const [stage, setStage]     = useState('')
  const [country, setCountry] = useState('')
  const [search, setSearch]   = useState('')

  const startups = allStartups.filter((s) => {
    if (sector  && s.sector  !== sector)  return false
    if (stage   && s.stage   !== stage)   return false
    if (country && s.country !== country) return false
    if (search  && !s.name.toLowerCase().includes(search.toLowerCase())) return false
    return true
  })

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

      <Card padding="sm">
        <Table
          headers={['Nombre', 'Sector', 'Subsector', 'Etapa', 'País', 'Estado', 'Datos']}
          rows={rows}
          onRowClick={(i) => router.push(`/portfolio/${encodeURIComponent(startups[i]?.name ?? '')}`)}
        />
      </Card>
    </PageWrapper>
  )
}
