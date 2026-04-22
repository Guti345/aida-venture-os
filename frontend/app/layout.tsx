import type { Metadata } from 'next'
import '../styles/globals.css'
import Sidebar from '@/components/layout/Sidebar'
import Topbar from '@/components/layout/Topbar'

export const metadata: Metadata = {
  title: 'AIDA Venture OS',
  description: 'Sistema operativo de decisión para venture capital y venture studio',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <div className="flex h-screen overflow-hidden">
          <Sidebar />
          <div className="flex flex-col flex-1 overflow-hidden">
            <Topbar />
            <main className="flex-1 overflow-y-auto bg-[#F5F7FA]">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}
