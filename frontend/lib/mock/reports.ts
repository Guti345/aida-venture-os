import type { LPReportSummary } from '../types'
import { portfolioSnapshot } from './portfolio'

export const lpReport: LPReportSummary = {
  fund_name: 'AIDA Ventures Fund I',
  report_date: '2026-04-21',
  total_invested_usd: 3150000,
  portfolio_companies: 10,
  fund_moic_current: 2.83,
  fund_irr_estimate_pct: 22.4,
  narrative_summary:
    'El portafolio de AIDA Ventures Fund I mantiene un desempeño sólido en el primer trimestre de 2026. ' +
    'LogiFlow lidera el portfolio con ARR de $3.2M y crecimiento MoM del 8%, posicionada para Serie B. ' +
    'CreditIA y FinStack consolidan su posición en el segmento Fintech colombiano con NRR superior al 118%. ' +
    'Las empresas del Venture Studio representan el 40% del portafolio activo con un costo de construcción ' +
    'promedio de $170K — 32% por debajo del benchmark de mercado LATAM. ' +
    'El fondo mantiene un runway promedio de 15 meses y exposición controlada en sectores regulados.',
}

export { portfolioSnapshot }
