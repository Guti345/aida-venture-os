'use client'

import clsx from 'clsx'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface KPICardProps {
  label: string
  value: string
  unit?: string
  delta?: number | null
  trend?: 'up' | 'down' | 'neutral'
  deltaLabel?: string
}

export default function KPICard({
  label,
  value,
  unit,
  delta,
  trend = 'neutral',
  deltaLabel,
}: KPICardProps) {
  const trendColor =
    trend === 'up'
      ? 'text-[#22C55E]'
      : trend === 'down'
      ? 'text-[#EF4444]'
      : 'text-[#9CA3AF]'

  const TrendIcon =
    trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus

  return (
    <div className="bg-white rounded-lg border border-[#9CA3AF]/20 shadow-sm p-6">
      <p className="text-sm font-medium text-[#9CA3AF] mb-1">{label}</p>
      <div className="flex items-baseline gap-1">
        <span className="text-2xl font-semibold text-[#0A0B0E]">{value}</span>
        {unit && (
          <span className="text-sm text-[#9CA3AF]">{unit}</span>
        )}
      </div>
      {delta !== null && delta !== undefined && (
        <div className={clsx('flex items-center gap-1 mt-2 text-sm', trendColor)}>
          <TrendIcon size={14} />
          <span>
            {delta > 0 ? '+' : ''}{delta}
            {deltaLabel ? ` ${deltaLabel}` : ''}
          </span>
        </div>
      )}
    </div>
  )
}
