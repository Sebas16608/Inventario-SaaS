import axios, { AxiosInstance } from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Agregar token a cada request
    this.client.interceptors.request.use((config) => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Manejar errores de autenticación
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  async getToken(email: string, password: string) {
    const response = await this.client.post('/auth/token/', { email, password })
    return response.data
  }

  async refreshToken(refresh: string) {
    const response = await this.client.post('/auth/token/refresh/', { refresh })
    return response.data
  }

  // Users
  async getUsers(params?: Record<string, any>) {
    const response = await this.client.get('/users/', { params })
    return response.data
  }

  async getUserProfile() {
    const response = await this.client.get('/users/me/')
    return response.data
  }

  async createUser(data: Record<string, any>) {
    const response = await this.client.post('/users/', data)
    return response.data
  }

  async updateUser(id: number, data: Record<string, any>) {
    const response = await this.client.put(`/users/${id}/`, data)
    return response.data
  }

  // Empresas
  async getEmpresas(params?: Record<string, any>) {
    const response = await this.client.get('/empresas/', { params })
    return response.data
  }

  async getEmpresaProfile() {
    const response = await this.client.get('/empresas/me/')
    return response.data
  }

  async createEmpresa(data: Record<string, any>) {
    const response = await this.client.post('/empresas/', data)
    return response.data
  }

  async updateEmpresa(id: number, data: Record<string, any>) {
    const response = await this.client.put(`/empresas/${id}/`, data)
    return response.data
  }

  // Categorías
  async getCategories(params?: Record<string, any>) {
    const response = await this.client.get('/categories/', { params })
    return response.data
  }

  async createCategory(data: Record<string, any>) {
    const response = await this.client.post('/categories/', data)
    return response.data
  }

  // Productos
  async getProducts(params?: Record<string, any>) {
    const response = await this.client.get('/products/', { params })
    return response.data
  }

  async getProduct(id: number) {
    const response = await this.client.get(`/products/${id}/`)
    return response.data
  }

  async createProduct(data: Record<string, any>) {
    const response = await this.client.post('/products/', data)
    return response.data
  }

  async updateProduct(id: number, data: Record<string, any>) {
    const response = await this.client.put(`/products/${id}/`, data)
    return response.data
  }

  // Movimientos
  async getMovements(params?: Record<string, any>) {
    const response = await this.client.get('/movements/', { params })
    return response.data
  }

  async createMovement(data: Record<string, any>) {
    const response = await this.client.post('/movements/', data)
    return response.data
  }
}

export const apiClient = new ApiClient()
