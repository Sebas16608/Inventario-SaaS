'use client'

import { useEffect, useState } from 'react'
import { apiClient } from '@/services/api'
import { Layout } from '@/components/Layout'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { Plus, Trash2, Edit2 } from 'lucide-react'
import Link from 'next/link'

interface Product {
  id: number
  codigo: string
  nombre: string
  descripcion: string
  precio_venta: number
  precio_costo: number
  categoria: number
  is_active: boolean
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadProducts()
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getProducts()
      setProducts(data.results || data)
    } catch (err: any) {
      setError('Error al cargar productos')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
      try {
        // Aquí iría la llamada a delete
        setProducts(products.filter(p => p.id !== id))
      } catch (err) {
        setError('Error al eliminar producto')
      }
    }
  }

  return (
    <ProtectedRoute>
      <Layout>
        <div>
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Productos</h1>
              <p className="text-gray-600 mt-2">Gestiona tu inventario de productos</p>
            </div>
            <Link
              href="/products/new"
              className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition"
            >
              <Plus size={20} />
              Nuevo Producto
            </Link>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {/* Products Table */}
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          ) : products.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-600 text-lg mb-4">No hay productos registrados</p>
              <Link
                href="/products/new"
                className="inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition"
              >
                <Plus size={20} />
                Crear Producto
              </Link>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Código</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Nombre</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Descripción</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Precio Venta</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Precio Costo</th>
                    <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {products.map((product) => (
                    <tr key={product.id} className="border-b border-gray-200 hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm text-gray-900">{product.codigo}</td>
                      <td className="px-6 py-4 text-sm font-medium text-gray-900">{product.nombre}</td>
                      <td className="px-6 py-4 text-sm text-gray-600">{product.descripcion}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">${product.precio_venta.toFixed(2)}</td>
                      <td className="px-6 py-4 text-sm text-gray-900">${product.precio_costo.toFixed(2)}</td>
                      <td className="px-6 py-4 text-sm">
                        <div className="flex items-center gap-2">
                          <Link
                            href={`/products/${product.id}`}
                            className="text-blue-600 hover:text-blue-700"
                          >
                            <Edit2 size={18} />
                          </Link>
                          <button
                            onClick={() => handleDelete(product.id)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
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
