'use client'

import clsx from 'clsx'

interface PageWrapperProps {
  children: React.ReactNode
  className?: string
}

export default function PageWrapper({ children, className }: PageWrapperProps) {
  return (
    <div className={clsx('p-6 max-w-[1400px] mx-auto space-y-6', className)}>
      {children}
    </div>
  )
}
