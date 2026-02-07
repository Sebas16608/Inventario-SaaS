'use client'

import { useEffect, useState } from 'react'
import { useAuthStore } from '@/store/auth'
import { apiClient } from '@/services/api'
import { Layout } from '@/components/Layout'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { Package, TrendingUp, Users, Zap } from 'lucide-react'

interface DashboardStats {
  totalProducts: number
  totalMovements: number
  activeUsers: number
}

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<DashboardStats>({
    totalProducts: 0,
    totalMovements: 0,
    activeUsers: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadStats = async () => {
      try {
        const [productsData, movementsData, usersData] = await Promise.all([
          apiClient.getProducts({ limit: 1 }),
          apiClient.getMovements({ limit: 1 }),
          apiClient.getUsers({ limit: 1 }),
        ])

        setStats({
          totalProducts: productsData.count || 0,
          totalMovements: movementsData.count || 0,
          activeUsers: usersData.count || 0,
        })
      } catch (error) {
        console.error('Error loading stats:', error)
      } finally {
        setLoading(false)
      }
    }

    loadStats()
  }, [])

  return (
    <ProtectedRoute>
      <Layout>
        <div>
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">
              Bienvenido, {user?.first_name}! 👋
            </h1>
            <p className="text-gray-600 mt-2">
              Aquí está un resumen de tu inventario
            </p>
          </div>

          {/* Stats Grid */}
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Productos */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium">Total de Productos</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">
                      {stats.totalProducts}
                    </p>
                  </div>
                  <div className="bg-blue-100 rounded-lg p-3">
                    <Package className="text-blue-600" size={24} />
                  </div>
                </div>
              </div>

              {/* Movimientos */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium">Movimientos</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">
                      {stats.totalMovements}
                    </p>
                  </div>
                  <div className="bg-green-100 rounded-lg p-3">
                    <TrendingUp className="text-green-600" size={24} />
                  </div>
                </div>
              </div>

              {/* Usuarios */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium">Usuarios Activos</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">
                      {stats.activeUsers}
                    </p>
                  </div>
                  <div className="bg-purple-100 rounded-lg p-3">
                    <Users className="text-purple-600" size={24} />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Acciones Rápidas</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <a
                href="/products"
                className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
              >
                <Package className="text-primary-600" size={20} />
                <div>
                  <p className="font-semibold text-gray-900">Ver Productos</p>
                  <p className="text-sm text-gray-600">Gestiona tu inventario</p>
                </div>
              </a>

              <a
                href="/movements"
                className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
              >
                <TrendingUp className="text-primary-600" size={20} />
                <div>
                  <p className="font-semibold text-gray-900">Movimientos</p>
                  <p className="text-sm text-gray-600">Historial de cambios</p>
                </div>
              </a>

              <a
                href="/products/new"
                className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
              >
                <Zap className="text-primary-600" size={20} />
                <div>
                  <p className="font-semibold text-gray-900">Nuevo Producto</p>
                  <p className="text-sm text-gray-600">Agrega un producto nuevo</p>
                </div>
              </a>

              <a
                href="/movements/new"
                className="flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
              >
                <Package className="text-primary-600" size={20} />
                <div>
                  <p className="font-semibold text-gray-900">Nuevo Movimiento</p>
                  <p className="text-sm text-gray-600">Registra un movimiento</p>
                </div>
              </a>
            </div>
          </div>
        </div>
      </Layout>
    </ProtectedRoute>
  )
}
