import { create } from 'zustand'
import { apiClient } from '@/services/api'

interface User {
  id: number
  email: string
  username: string
  first_name: string
  last_name: string
  telefono?: string
  empresa: number
  is_active: boolean
}

interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Actions
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null })
    try {
      const data = await apiClient.getToken(email, password)
      console.log('Login successful:', { access: data.access ? 'present' : 'missing' })
      
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)

      // Obtener perfil del usuario
      const userProfile = await apiClient.getUserProfile()
      console.log('User profile fetched:', userProfile)
      
      set({
        token: data.access,
        refreshToken: data.refresh,
        user: userProfile,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (error: any) {
      console.error('Login error:', error.response?.data || error.message)
      set({
        error: error.response?.data?.detail || error.message || 'Error al iniciar sesión',
        isLoading: false,
      })
      throw error
    }
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
    })
  },

  setUser: (user: User) => {
    set({ user })
  },

  checkAuth: async () => {
    set({ isLoading: true })
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        set({ token, isAuthenticated: true })
        const userProfile = await apiClient.getUserProfile()
        set({ user: userProfile, isLoading: false })
      } catch (error: any) {
        console.error('Auth check failed:', error)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
        })
      }
    } else {
      set({ isLoading: false })
    }
  },
}))
