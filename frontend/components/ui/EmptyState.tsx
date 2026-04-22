'use client'

import { Inbox } from 'lucide-react'

interface EmptyStateProps {
  title: string
  description?: string
  icon?: React.ReactNode
}

export default function EmptyState({ title, description, icon }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-[#9CA3AF] mb-3">
        {icon ?? <Inbox size={36} strokeWidth={1.5} />}
      </div>
      <p className="text-sm font-medium text-[#0A0B0E]">{title}</p>
      {description && (
        <p className="text-sm text-[#9CA3AF] mt-1 max-w-xs">{description}</p>
      )}
    </div>
  )
}
