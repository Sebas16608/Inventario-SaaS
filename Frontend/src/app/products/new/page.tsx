'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { apiClient } from '@/services/api'
import { Layout } from '@/components/Layout'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { ArrowLeft, Loader } from 'lucide-react'
import Link from 'next/link'

interface Category {
  id: number
  nombre: string
}

export default function NewProductPage() {
  const router = useRouter()
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(false)
  const [submitLoading, setSubmitLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    codigo: '',
    nombre: '',
    descripcion: '',
    precio_venta: 0,
    precio_costo: 0,
    categoria: '',
  })

  useEffect(() => {
    loadCategories()
  }, [])

  const loadCategories = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getCategories()
      setCategories(data.results || data)
    } catch (err: any) {
      setError('Error al cargar categorías')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name.startsWith('precio') || name === 'categoria' ? (value === '' ? '' : (name === 'categoria' ? value : parseFloat(value) || 0)) : value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!formData.codigo || !formData.nombre || !formData.categoria) {
      setError('Por favor completa todos los campos requeridos')
      return
    }

    try {
      setSubmitLoading(true)
      await apiClient.createProduct({
        codigo: formData.codigo,
        nombre: formData.nombre,
        descripcion: formData.descripcion,
        precio_venta: formData.precio_venta,
        precio_costo: formData.precio_costo,
        categoria: parseInt(formData.categoria as string),
      })
      router.push('/products')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al crear producto')
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
              href="/products"
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ArrowLeft className="text-gray-600" size={20} />
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Nuevo Producto</h1>
              <p className="text-gray-600 mt-2">Agrega un nuevo producto a tu inventario</p>
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
              {/* Código */}
              <div>
                <label htmlFor="codigo" className="block text-sm font-medium text-gray-700 mb-2">
                  Código *
                </label>
                <input
                  id="codigo"
                  type="text"
                  name="codigo"
                  value={formData.codigo}
                  onChange={handleChange}
                  placeholder="Ej: PROD-001"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>

              {/* Nombre */}
              <div>
                <label htmlFor="nombre" className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre *
                </label>
                <input
                  id="nombre"
                  type="text"
                  name="nombre"
                  value={formData.nombre}
                  onChange={handleChange}
                  placeholder="Nombre del producto"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>

              {/* Categoría */}
              <div>
                <label htmlFor="categoria" className="block text-sm font-medium text-gray-700 mb-2">
                  Categoría *
                </label>
                {loading ? (
                  <div className="text-gray-500">Cargando categorías...</div>
                ) : (
                  <select
                    id="categoria"
                    name="categoria"
                    value={formData.categoria}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Selecciona una categoría</option>
                    {categories.map(cat => (
                      <option key={cat.id} value={cat.id}>
                        {cat.nombre}
                      </option>
                    ))}
                  </select>
                )}
              </div>

              {/* Precio Costo */}
              <div>
                <label htmlFor="precio_costo" className="block text-sm font-medium text-gray-700 mb-2">
                  Precio Costo
                </label>
                <input
                  id="precio_costo"
                  type="number"
                  name="precio_costo"
                  value={formData.precio_costo}
                  onChange={handleChange}
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>

              {/* Precio Venta */}
              <div>
                <label htmlFor="precio_venta" className="block text-sm font-medium text-gray-700 mb-2">
                  Precio Venta
                </label>
                <input
                  id="precio_venta"
                  type="number"
                  name="precio_venta"
                  value={formData.precio_venta}
                  onChange={handleChange}
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Descripción */}
            <div className="mt-6">
              <label htmlFor="descripcion" className="block text-sm font-medium text-gray-700 mb-2">
                Descripción
              </label>
              <textarea
                id="descripcion"
                name="descripcion"
                value={formData.descripcion}
                onChange={handleChange}
                placeholder="Descripción del producto"
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
                  'Guardar Producto'
                )}
              </button>
              <Link
                href="/products"
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
