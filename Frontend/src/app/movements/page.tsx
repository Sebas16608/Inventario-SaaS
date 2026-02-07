'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/services/api'
import { Layout } from '@/components/Layout'
import { ProtectedRoute } from '@/components/ProtectedRoute'

interface Movement {
  id: number
  producto: string
  tipo: 'ENTRADA' | 'SALIDA'
  cantidad: number
  razon: string
  created_at: string
}

export default function MovementsPage() {
  const [movements, setMovements] = useState<Movement[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadMovements()
  }, [])

  const loadMovements = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getMovements()
      setMovements(data.results || data)
    } catch (err: any) {
      setError('Error al cargar movimientos')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <ProtectedRoute>
      <Layout>
        <div>
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Movimientos de Inventario</h1>
            <p className="text-gray-600 mt-2">Historial de entradas y salidas</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {/* Movements Table */}
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          ) : movements.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-600 text-lg">No hay movimientos registrados</p>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Producto</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Tipo</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Cantidad</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Razón</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Fecha</th>
                  </tr>
                </thead>
                <tbody>
                  {movements.map((movement) => (
                    <tr key={movement.id} className="border-b border-gray-200 hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm text-gray-900">{movement.producto}</td>
                      <td className="px-6 py-4 text-sm">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            movement.tipo === 'ENTRADA'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {movement.tipo}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900">{movement.cantidad}</td>
                      <td className="px-6 py-4 text-sm text-gray-600">{movement.razon}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">
                        {new Date(movement.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </Layout>
    </ProtectedRoute>
  )
}
