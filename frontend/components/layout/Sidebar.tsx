'use client'

import { useState } from 'react'
import { usePathname } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import clsx from 'clsx'
import {
  ChevronDown,
  ChevronRight,
  LayoutDashboard,
} from 'lucide-react'

interface NavItem {
  label: string
  href: string
}

interface NavSection {
  label: string
  items: NavItem[]
}

const navSections: NavSection[] = [
  {
    label: 'PORTAFOLIO',
    items: [
      { label: 'Portfolio Overview',  href: '/portfolio' },
      { label: 'Startup Detail',      href: '/portfolio' },
      { label: 'Métricas',            href: '/portfolio' },
    ],
  },
  {
    label: 'FONDO',
    items: [
      { label: 'Fund Overview',           href: '/fund' },
      { label: 'Simulador Monte Carlo',   href: '/fund' },
    ],
  },
  {
    label: 'VENTURE STUDIO',
    items: [
      { label: 'Studio Overview',  href: '/studio' },
      { label: 'Empresas',         href: '/studio' },
      { label: 'Alpha Metrics',    href: '/studio' },
    ],
  },
  {
    label: 'DEALS',
    items: [
      { label: 'Pipeline',          href: '/deals' },
      { label: 'Sourcing Channels', href: '/deals' },
      { label: 'IC Memos',         href: '/deals' },
    ],
  },
  {
    label: 'MERCADO',
    items: [
      { label: 'Benchmarks', href: '/market' },
      { label: 'Segmentos',  href: '/market' },
    ],
  },
  {
    label: 'REPORTES',
    items: [
      { label: 'LP Summary',         href: '/reports' },
      { label: 'Portfolio Snapshot', href: '/reports' },
    ],
  },
]

function isActive(pathname: string, href: string): boolean {
  if (href === '/') return pathname === '/'
  return pathname === href || pathname.startsWith(href + '/')
}

export default function Sidebar() {
  const pathname = usePathname()
  const [open, setOpen] = useState<Record<string, boolean>>(
    Object.fromEntries(navSections.map((s) => [s.label, true]))
  )

  const toggle = (label: string) =>
    setOpen((prev) => ({ ...prev, [label]: !prev[label] }))

  return (
    <aside className="w-64 h-screen bg-[#0B1628] text-white flex flex-col flex-shrink-0 overflow-hidden">
      {/* Logo */}
      <div className="flex items-center gap-3 px-5 py-5 border-b border-white/10">
        <div className="w-8 h-8 flex-shrink-0 relative">
          <Image
            src="/logo.png"
            alt="AIDA Ventures"
            fill
            className="object-contain"
            priority
          />
        </div>
        <span className="text-sm font-semibold text-white tracking-wide">AIDA Ventures</span>
      </div>

      {/* Dashboard link */}
      <div className="px-3 pt-4">
        <Link
          href="/"
          className={clsx(
            'flex items-center gap-2 px-3 py-2 rounded text-sm transition-colors',
            pathname === '/'
              ? 'border-l-2 border-[#1A6FE8] bg-[#1A6FE8]/15 text-white pl-[10px]'
              : 'text-white/60 hover:text-white hover:bg-white/5'
          )}
        >
          <LayoutDashboard size={15} />
          Dashboard
        </Link>
      </div>

      {/* Nav sections */}
      <nav className="flex-1 overflow-y-auto px-3 py-3 space-y-1">
        {navSections.map((section) => {
          const sectionActive = section.items.some((item) => isActive(pathname, item.href))
          const isOpen = open[section.label] ?? true

          return (
            <div key={section.label}>
              <button
                onClick={() => toggle(section.label)}
                className={clsx(
                  'w-full flex items-center justify-between px-3 py-1.5 mt-2 rounded transition-colors',
                  'text-[10px] font-bold tracking-widest uppercase',
                  sectionActive ? 'text-white/80' : 'text-white/35 hover:text-white/50'
                )}
              >
                {section.label}
                {isOpen ? (
                  <ChevronDown size={12} />
                ) : (
                  <ChevronRight size={12} />
                )}
              </button>

              {isOpen && (
                <div className="mt-0.5 space-y-0.5">
                  {section.items.map((item, idx) => {
                    const active = isActive(pathname, item.href)
                    return (
                      <Link
                        key={idx}
                        href={item.href}
                        className={clsx(
                          'flex items-center text-sm rounded transition-colors py-1.5',
                          active
                            ? 'border-l-2 border-[#1A6FE8] bg-[#1A6FE8]/15 text-white px-[10px]'
                            : 'text-white/55 hover:text-white hover:bg-white/5 px-3'
                        )}
                      >
                        {item.label}
                      </Link>
                    )
                  })}
                </div>
              )}
            </div>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="px-5 py-4 border-t border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-full bg-[#1A6FE8] flex items-center justify-center flex-shrink-0">
            <span className="text-white text-xs font-semibold">A</span>
          </div>
          <p className="text-xs text-white/40 truncate">admin@aidaventures.co</p>
        </div>
      </div>
    </aside>
  )
}
