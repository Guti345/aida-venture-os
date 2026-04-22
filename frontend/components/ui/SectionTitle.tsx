'use client'

interface SectionTitleProps {
  title: string
  subtitle?: string
  className?: string
}

export default function SectionTitle({ title, subtitle, className }: SectionTitleProps) {
  return (
    <div className={className}>
      <h2 className="text-lg font-semibold text-[#0A0B0E]">{title}</h2>
      {subtitle && (
        <p className="text-sm text-[#9CA3AF] mt-0.5">{subtitle}</p>
      )}
    </div>
  )
}
