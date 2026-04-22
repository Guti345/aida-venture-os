'use client'

import { usePathname } from 'next/navigation'

const routeTitles: [string, string][] = [
  ['/portfolio', 'Portfolio Overview'],
  ['/fund',      'Fund Simulator'],
  ['/studio',    'Venture Studio'],
  ['/deals',     'Deal Pipeline'],
  ['/market',    'Market Benchmarks'],
  ['/reports',   'LP Reports'],
  ['/',          'Dashboard'],
]

function getTitle(pathname: string): string {
  for (const [prefix, title] of routeTitles) {
    if (pathname === prefix || (prefix !== '/' && pathname.startsWith(prefix + '/'))) {
      return title
    }
  }
  return 'AIDA Venture OS'
}

export default function Topbar() {
  const pathname = usePathname()
  const title = getTitle(pathname)

  return (
    <header className="h-14 bg-white border-b border-[#9CA3AF]/20 flex items-center justify-between px-6 flex-shrink-0">
      <h1 className="text-base font-semibold text-[#0A0B0E]">{title}</h1>
      <div className="flex items-center gap-3">
        <span className="text-sm text-[#9CA3AF] hidden sm:block">admin@aidaventures.co</span>
        <div className="w-8 h-8 rounded-full bg-[#1A6FE8] flex items-center justify-center flex-shrink-0">
          <span className="text-white text-sm font-semibold">A</span>
        </div>
      </div>
    </header>
  )
}
