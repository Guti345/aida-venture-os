'use client'

import clsx from 'clsx'

interface CardProps {
  children: React.ReactNode
  className?: string
  padding?: 'sm' | 'md' | 'lg'
}

export default function Card({ children, className, padding = 'md' }: CardProps) {
  const paddings = { sm: 'p-4', md: 'p-6', lg: 'p-8' }

  return (
    <div
      className={clsx(
        'bg-white rounded-lg border border-[#9CA3AF]/20 shadow-sm',
        paddings[padding],
        className
      )}
    >
      {children}
    </div>
  )
}
