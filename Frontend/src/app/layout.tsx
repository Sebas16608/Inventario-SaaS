import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import '@/globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Inventario SaaS | Dashboard de Gestión de Inventario',
  description: 'Sistema de gestión de inventario multi-tenant para pequeñas y medianas empresas',
  keywords: 'inventario, gestión, saas, farmacia, veterinaria',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
