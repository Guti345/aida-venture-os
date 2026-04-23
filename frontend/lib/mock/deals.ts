import type { DealOpportunity, SourcingChannel } from '../types'

export const channels: SourcingChannel[] = [
  { id: 'ch-001', name: 'Red de LPs',         channel_type: 'network',    is_active: true, deals_count: 3 },
  { id: 'ch-002', name: 'Aceleradoras LATAM',  channel_type: 'accelerator',is_active: true, deals_count: 2 },
  { id: 'ch-003', name: 'Inbound directo',     channel_type: 'inbound',    is_active: true, deals_count: 2 },
  { id: 'ch-004', name: 'Co-inversión',        channel_type: 'co_invest',  is_active: true, deals_count: 1 },
]

export const deals: DealOpportunity[] = [
  {
    id: 'deal-001',
    status: 'screening',
    startup_name: 'FinStack',
    sourcing_channel_name: 'Inbound directo',
    identified_at: '2025-03-10',
    avg_thesis_score: 72,
    days_in_pipeline: 42,
  },
  {
    id: 'deal-002',
    status: 'invested',
    startup_name: 'LogiFlow',
    sourcing_channel_name: 'Red de LPs',
    identified_at: '2023-09-15',
    avg_thesis_score: 88,
    days_in_pipeline: 0,
  },
  {
    id: 'deal-003',
    status: 'due_diligence',
    startup_name: 'TechCo Analytics',
    sourcing_channel_name: 'Aceleradoras LATAM',
    identified_at: '2025-02-20',
    avg_thesis_score: 65,
    days_in_pipeline: 60,
  },
  {
    id: 'deal-004',
    status: 'term_sheet',
    startup_name: 'CloudBase',
    sourcing_channel_name: 'Red de LPs',
    identified_at: '2025-01-08',
    avg_thesis_score: 80,
    days_in_pipeline: 103,
  },
  {
    id: 'deal-005',
    status: 'passed',
    startup_name: 'DataFlow',
    sourcing_channel_name: 'Inbound directo',
    identified_at: '2024-11-05',
    avg_thesis_score: 45,
    days_in_pipeline: 0,
  },
  {
    id: 'deal-006',
    status: 'screening',
    startup_name: 'HealthOS',
    sourcing_channel_name: 'Aceleradoras LATAM',
    identified_at: '2025-04-01',
    avg_thesis_score: 58,
    days_in_pipeline: 20,
  },
  {
    id: 'deal-007',
    status: 'due_diligence',
    startup_name: 'RetailAI',
    sourcing_channel_name: 'Co-inversión',
    identified_at: '2025-02-14',
    avg_thesis_score: 70,
    days_in_pipeline: 66,
  },
  {
    id: 'deal-008',
    status: 'screening',
    startup_name: 'GreenTech',
    sourcing_channel_name: 'Red de LPs',
    identified_at: '2025-04-10',
    avg_thesis_score: 62,
    days_in_pipeline: 11,
  },
]

export const dealsByStatus = {
  screening: 3,
  due_diligence: 2,
  term_sheet: 1,
  invested: 1,
  passed: 1,
}
