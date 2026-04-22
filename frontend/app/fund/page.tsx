'use client'

import { useState, useEffect } from 'react'
import PageWrapper from '@/components/layout/PageWrapper'
import Card from '@/components/ui/Card'
import KPICard from '@/components/ui/KPICard'
import SectionTitle from '@/components/ui/SectionTitle'
import Table from '@/components/ui/Table'
import { getFund, getFundMetrics, getFundInvestments, getFundScenarios, simulateFund } from '@/lib/api'
import type { FundData, FundMetrics, Investment, ScenarioResult } from '@/lib/types'

const fmtUSD = (v: number) =>
  v >= 1_000_000 ? `$${(v / 1_000_000).toFixed(2)}M` : `$${(v / 1_000).toFixed(0)}K`

const scenarioPresets: Record<string, { pct_winners: number; winner_multiple: number }> = {
  conservador: { pct_winners: 10, winner_multiple: 10 },
  base:        { pct_winners: 20, winner_multiple: 15 },
  optimista:   { pct_winners: 30, winner_multiple: 25 },
}

export default function FundPage() {
  const [fund, setFund]             = useState<FundData | null>(null)
  const [metrics, setMetrics]       = useState<FundMetrics | null>(null)
  const [investments, setInvestments] = useState<Investment[]>([])
  const [scenarios, setScenarios]   = useState<ScenarioResult[]>([])
  const [result, setResult]         = useState<ScenarioResult | null>(null)
  const [loading, setLoading]       = useState(false)

  const [label, setLabel]           = useState<'conservador' | 'base' | 'optimista'>('base')
  const [pctWinners, setPctWinners] = useState(20)
  const [winMult, setWinMult]       = useState(15)

  useEffect(() => {
    Promise.all([getFund(), getFundMetrics(), getFundInvestments(), getFundScenarios()]).then(
      ([f, m, inv, sc]) => {
        setFund(f)
        setMetrics(m)
        setInvestments(inv)
        setScenarios(sc)
        const base = sc.find((s) => s.label === 'base')
        if (base) setResult(base)
      }
    )
  }, [])

  const handleLabelChange = (l: 'conservador' | 'base' | 'optimista') => {
    setLabel(l)
    const preset = scenarioPresets[l]
    setPctWinners(preset.pct_winners)
    setWinMult(preset.winner_multiple)
  }

  const handleSimulate = async () => {
    setLoading(true)
    const res = await simulateFund({ scenario_label: label, pct_winners: pctWinners, winner_multiple: winMult })
    setResult(res)
    setLoading(false)
  }

  const invRows = investments.map((inv) => [
    <span key="name" className="font-medium">{inv.startup_name}</span>,
    fmtUSD(inv.amount_usd),
    inv.stage_at_entry,
    `${inv.ownership_pct}%`,
    new Date(inv.entry_date).toLocaleDateString('es-CO', { year: 'numeric', month: 'short' }),
  ])

  const scenarioRows = scenarios.map((s) => [
    <span key="label" className="capitalize font-medium">{s.label}</span>,
    `${s.moic_p25.toFixed(1)}x`,
    `${s.moic_p50.toFixed(1)}x`,
    `${s.moic_p75.toFixed(1)}x`,
    `${s.irr_p50.toFixed(1)}%`,
  ])

  return (
    <PageWrapper>
      {/* Fund KPIs */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard label="Fondo" value={fund?.name?.split(' ').slice(-2).join(' ') ?? '—'} />
        <KPICard label="Capital desplegado" value={fund ? fmtUSD(fund.deployed_usd) : '—'} />
        <KPICard label="MOIC actual" value={metrics ? `${metrics.moic_current.toFixed(2)}x` : '—'} trend="up" />
        <KPICard label="IRR estimado" value={metrics ? `${metrics.irr_estimate_pct.toFixed(1)}%` : '—'} trend="up" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Simulator form */}
        <Card>
          <SectionTitle title="Simulador Monte Carlo" subtitle="Configura el escenario y ejecuta la simulación" className="mb-6" />

          <div className="space-y-5">
            {/* Scenario selector */}
            <div>
              <label className="block text-sm font-medium text-[#0A0B0E] mb-2">Escenario</label>
              <div className="flex gap-2">
                {(['conservador', 'base', 'optimista'] as const).map((l) => (
                  <button
                    key={l}
                    onClick={() => handleLabelChange(l)}
                    className={`flex-1 py-2 rounded text-sm font-medium capitalize transition-colors ${
                      label === l
                        ? 'bg-[#1A6FE8] text-white'
                        : 'bg-[#F5F7FA] text-[#9CA3AF] hover:bg-[#E5E7EB]'
                    }`}
                  >
                    {l}
                  </button>
                ))}
              </div>
            </div>

            {/* % Winners */}
            <div>
              <div className="flex justify-between mb-1">
                <label className="text-sm font-medium text-[#0A0B0E]">% Ganadores</label>
                <span className="text-sm text-[#1A6FE8] font-semibold">{pctWinners}%</span>
              </div>
              <input
                type="range" min={5} max={50} step={1}
                value={pctWinners}
                onChange={(e) => setPctWinners(Number(e.target.value))}
                className="w-full accent-[#1A6FE8]"
              />
              <div className="flex justify-between text-xs text-[#9CA3AF] mt-1">
                <span>5%</span><span>50%</span>
              </div>
            </div>

            {/* Winner multiple */}
            <div>
              <div className="flex justify-between mb-1">
                <label className="text-sm font-medium text-[#0A0B0E]">Múltiplo ganador promedio</label>
                <span className="text-sm text-[#1A6FE8] font-semibold">{winMult}x</span>
              </div>
              <input
                type="range" min={3} max={50} step={1}
                value={winMult}
                onChange={(e) => setWinMult(Number(e.target.value))}
                className="w-full accent-[#1A6FE8]"
              />
              <div className="flex justify-between text-xs text-[#9CA3AF] mt-1">
                <span>3x</span><span>50x</span>
              </div>
            </div>

            <button
              onClick={handleSimulate}
              disabled={loading}
              className="w-full py-2.5 rounded bg-[#1A6FE8] text-white text-sm font-semibold hover:bg-[#1558c9] transition-colors disabled:opacity-50"
            >
              {loading ? 'Simulando...' : 'Ejecutar simulación'}
            </button>
          </div>
        </Card>

        {/* Results */}
        <div className="space-y-4">
          {result && (
            <Card>
              <SectionTitle title="Resultado" subtitle={`Escenario: ${result.label}`} className="mb-4" />
              <div className="grid grid-cols-3 gap-3 mb-4">
                <div className="bg-[#F5F7FA] rounded-lg p-3 text-center">
                  <p className="text-xs text-[#9CA3AF] mb-1">MOIC P25</p>
                  <p className="text-xl font-semibold text-[#0A0B0E]">{result.moic_p25.toFixed(1)}x</p>
                </div>
                <div className="bg-[#1A6FE8]/5 border border-[#1A6FE8]/20 rounded-lg p-3 text-center">
                  <p className="text-xs text-[#1A6FE8] mb-1">MOIC P50</p>
                  <p className="text-xl font-semibold text-[#1A6FE8]">{result.moic_p50.toFixed(1)}x</p>
                </div>
                <div className="bg-[#F5F7FA] rounded-lg p-3 text-center">
                  <p className="text-xs text-[#9CA3AF] mb-1">MOIC P75</p>
                  <p className="text-xl font-semibold text-[#0A0B0E]">{result.moic_p75.toFixed(1)}x</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-[#F5F7FA] rounded-lg p-3 text-center">
                  <p className="text-xs text-[#9CA3AF] mb-1">IRR P25</p>
                  <p className="text-xl font-semibold text-[#0A0B0E]">{result.irr_p25.toFixed(1)}%</p>
                </div>
                <div className="bg-[#22C55E]/5 border border-[#22C55E]/20 rounded-lg p-3 text-center">
                  <p className="text-xs text-[#22C55E] mb-1">IRR P50</p>
                  <p className="text-xl font-semibold text-[#22C55E]">{result.irr_p50.toFixed(1)}%</p>
                </div>
                <div className="bg-[#F5F7FA] rounded-lg p-3 text-center">
                  <p className="text-xs text-[#9CA3AF] mb-1">IRR P75</p>
                  <p className="text-xl font-semibold text-[#0A0B0E]">{result.irr_p75.toFixed(1)}%</p>
                </div>
              </div>
            </Card>
          )}

          <Card padding="sm">
            <SectionTitle title="Escenarios guardados" className="mb-3 px-2" />
            <Table
              headers={['Escenario', 'MOIC P25', 'MOIC P50', 'MOIC P75', 'IRR P50']}
              rows={scenarioRows}
            />
          </Card>
        </div>
      </div>

      {/* Investments */}
      <Card padding="sm">
        <SectionTitle title="Inversiones del fondo" className="mb-4 px-2" />
        <Table
          headers={['Startup', 'Monto', 'Etapa entrada', 'Participación', 'Fecha']}
          rows={invRows}
        />
      </Card>
    </PageWrapper>
  )
}
