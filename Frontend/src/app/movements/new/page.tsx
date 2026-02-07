'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/services/api'
import { Layout } from '@/components/Layout'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { ArrowLeft, Loader } from 'lucide-react'
import Link from 'next/link'

interface Product {
  id: number
  nombre: string
  codigo: string
}

export default function NewMovementPage() {
  const router = useRouter()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(false)
  const [submitLoading, setSubmitLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    producto: '',
    tipo: 'ENTRADA',
    cantidad: 1,
    razon: '',
  })

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'cantidad' ? (value === '' ? 1 : parseInt(value) || 1) : value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!formData.producto || !formData.cantidad) {
      setError('Por favor completa los campos requeridos')
      return
    }

    try {
      setSubmitLoading(true)
      await apiClient.createMovement({
        producto: parseInt(formData.producto),
        tipo: formData.tipo,
        cantidad: formData.cantidad,
        razon: formData.razon,
      })
      router.push('/movements')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al registrar movimiento')
      console.error(err)
    } finally {
      setSubmitLoading(false)
    }
  }

  return (
    <ProtectedRoute>
      <Layout>
        <div>
          {/* Header */}
          <div className="flex items-center gap-4 mb-8">
            <Link
              href="/movements"
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ArrowLeft className="text-gray-600" size={20} />
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Nuevo Movimiento</h1>
              <p className="text-gray-600 mt-2">Registra una entrada o salida de producto</p>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-8 max-w-2xl">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Producto */}
              <div className="md:col-span-1">
                <label htmlFor="producto" className="block text-sm font-medium text-gray-700 mb-2">
                  Producto *
                </label>
                {loading ? (
                  <div className="text-gray-500">Cargando productos...</div>
                ) : (
                  <select
                    id="producto"
                    name="producto"
                    value={formData.producto}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Selecciona un producto</option>
                    {products.map(prod => (
                      <option key={prod.id} value={prod.id}>
                        {prod.codigo} - {prod.nombre}
                      </option>
                    ))}
                  </select>
                )}
              </div>

              {/* Tipo */}
              <div className="md:col-span-1">
                <label htmlFor="tipo" className="block text-sm font-medium text-gray-700 mb-2">
                  Tipo de Movimiento *
                </label>
                <select
                  id="tipo"
                  name="tipo"
                  value={formData.tipo}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="ENTRADA">Entrada (Ingreso)</option>
                  <option value="SALIDA">Salida (Egreso)</option>
                </select>
              </div>

              {/* Cantidad */}
              <div className="md:col-span-1">
                <label htmlFor="cantidad" className="block text-sm font-medium text-gray-700 mb-2">
                  Cantidad *
                </label>
                <input
                  id="cantidad"
                  type="number"
                  name="cantidad"
                  value={formData.cantidad}
                  onChange={handleChange}
                  min="1"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Razón */}
            <div className="mt-6">
              <label htmlFor="razon" className="block text-sm font-medium text-gray-700 mb-2">
                Razón / Observaciones
              </label>
              <textarea
                id="razon"
                name="razon"
                value={formData.razon}
                onChange={handleChange}
                placeholder="Describe por qué se realiza este movimiento (ej: Compra a proveedor, Venta cliente, etc.)"
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            {/* Buttons */}
            <div className="flex gap-4 mt-8">
              <button
                type="submit"
                disabled={submitLoading}
                className="flex-1 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg transition flex items-center justify-center gap-2"
              >
                {submitLoading ? (
                  <>
                    <Loader size={18} className="animate-spin" />
                    Guardando...
                  </>
                ) : (
                  'Registrar Movimiento'
                )}
              </button>
              <Link
                href="/movements"
                className="flex-1 border border-gray-300 hover:bg-gray-50 text-gray-700 px-6 py-2 rounded-lg transition text-center"
              >
                Cancelar
              </Link>
            </div>
          </form>
        </div>
      </Layout>
    </ProtectedRoute>
  )
}
