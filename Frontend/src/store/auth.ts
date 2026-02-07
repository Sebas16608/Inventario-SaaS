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
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)

      // Obtener perfil del usuario
      const userProfile = await apiClient.getUserProfile()
      set({
        token: data.access,
        refreshToken: data.refresh,
        user: userProfile,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (error: any) {
      set({
        error: error.response?.data?.detail || 'Error al iniciar sesión',
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
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        set({ token, isAuthenticated: true })
        const userProfile = await apiClient.getUserProfile()
        set({ user: userProfile })
      } catch (error) {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      }
    }
  },
}))
