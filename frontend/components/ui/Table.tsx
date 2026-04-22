'use client'

import clsx from 'clsx'

interface TableProps {
  headers: string[]
  rows: React.ReactNode[][]
  onRowClick?: (index: number) => void
  className?: string
}

export default function Table({ headers, rows, onRowClick, className }: TableProps) {
  return (
    <div className={clsx('w-full overflow-x-auto', className)}>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-[#9CA3AF]/20">
            {headers.map((h) => (
              <th
                key={h}
                className="text-left py-3 px-4 text-xs font-semibold text-[#9CA3AF] uppercase tracking-wider whitespace-nowrap"
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr
              key={i}
              onClick={() => onRowClick?.(i)}
              className={clsx(
                'border-b border-[#9CA3AF]/10 transition-colors',
                onRowClick ? 'cursor-pointer hover:bg-[#F5F7FA]' : ''
              )}
            >
              {row.map((cell, j) => (
                <td key={j} className="py-3 px-4 text-[#0A0B0E]">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={headers.length} className="py-8 text-center text-[#9CA3AF] text-sm">
                Sin resultados
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
