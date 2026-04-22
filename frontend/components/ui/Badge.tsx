'use client'

import clsx from 'clsx'

type BadgeVariant =
  | 'active'
  | 'watchlist'
  | 'passed'
  | 'acquired'
  | 'invested'
  | 'screening'
  | 'due_diligence'
  | 'term_sheet'
  | 'archived'
  | 'default'

const variantStyles: Record<BadgeVariant, string> = {
  active:        'bg-[#22C55E]/10 text-[#22C55E] border-[#22C55E]/30',
  watchlist:     'bg-[#F5A623]/10 text-[#F5A623] border-[#F5A623]/30',
  passed:        'bg-[#9CA3AF]/10 text-[#9CA3AF] border-[#9CA3AF]/30',
  acquired:      'bg-[#1A6FE8]/10 text-[#1A6FE8] border-[#1A6FE8]/30',
  invested:      'bg-[#1A6FE8]/10 text-[#1A6FE8] border-[#1A6FE8]/30',
  screening:     'bg-[#F5A623]/10 text-[#F5A623] border-[#F5A623]/30',
  due_diligence: 'bg-[#1A6FE8]/10 text-[#1A6FE8] border-[#1A6FE8]/30',
  term_sheet:    'bg-[#0B1628]/10 text-[#0B1628] border-[#0B1628]/30',
  archived:      'bg-[#9CA3AF]/10 text-[#9CA3AF] border-[#9CA3AF]/30',
  default:       'bg-[#9CA3AF]/10 text-[#9CA3AF] border-[#9CA3AF]/30',
}

const labels: Record<string, string> = {
  active:        'Activo',
  watchlist:     'Watchlist',
  passed:        'Descartado',
  acquired:      'Adquirido',
  invested:      'Invertido',
  screening:     'Screening',
  due_diligence: 'Due Diligence',
  term_sheet:    'Term Sheet',
  archived:      'Archivado',
}

interface BadgeProps {
  value: string
  label?: string
}

export default function Badge({ value, label }: BadgeProps) {
  const variant = (value as BadgeVariant) in variantStyles ? (value as BadgeVariant) : 'default'
  const displayLabel = label ?? labels[value] ?? value

  return (
    <span
      className={clsx(
        'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border',
        variantStyles[variant]
      )}
    >
      {displayLabel}
    </span>
  )
}
