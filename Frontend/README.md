# Inventario-SaaS Frontend

Frontend moderno para el sistema de gestión de inventario multi-tenant **Inventario-SaaS**.

## 🚀 Características

- ✅ Autenticación JWT
- ✅ Dashboard interactivo
- ✅ Gestión de productos
- ✅ Historial de movimientos
- ✅ Diseño responsive con Tailwind CSS
- ✅ TypeScript para seguridad de tipos

## 🛠️ Stack Tecnológico

- **Next.js 14** - Framework React moderno
- **TypeScript** - Seguridad de tipos
- **Tailwind CSS** - Estilos utilities
- **Zustand** - State management
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos SVG

## 📦 Instalación

```bash
# Instalar dependencias
npm install

# Variables de entorno (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 🚀 Desarrollo

```bash
# Iniciar servidor de desarrollo
npm run dev

# Compilar proyecto
npm run build

# Iniciar servidor de producción
npm start

# Verificar tipos TypeScript
npm run type-check

# Formatear código
npm run format
```

El servidor estará disponible en `http://localhost:3000`

## 📁 Estructura del Proyecto

```
src/
├── app/               # App directory de Next.js 14
│   ├── layout.tsx     # Layout global
│   ├── page.tsx       # Página raíz
│   ├── login/         # Página de login
│   ├── dashboard/     # Dashboard
│   ├── products/      # Gestión de productos
│   └── movements/     # Historial de movimientos
├── components/        # Componentes reutilizables
│   ├── Layout.tsx     # Layout principal
│   ├── Navbar.tsx     # Barra de navegación
│   └── ProtectedRoute.tsx # Rutas protegidas
├── services/          # Servicios de API
│   └── api.ts         # Cliente HTTP
├── store/             # State management (Zustand)
│   └── auth.ts        # Store de autenticación
├── types/             # Tipos TypeScript
├── utils/             # Funciones utilitarias
├── hooks/             # Custom React hooks
└── globals.css        # Estilos globales
```

## 🔐 Autenticación

La autenticación se realiza mediante JWT tokens:

1. Usuario ingresa credenciales
2. Backend retorna `access_token` y `refresh_token`
3. Token se almacena en `localStorage`
4. Se agrega automáticamente a todos los requests

## 🌐 Integración con Backend

El frontend se conecta al backend en `http://localhost:8000/api`:

```typescript
// Ejemplo de uso
import { apiClient } from '@/services/api'

// Obtener productos
const products = await apiClient.getProducts()

// Crear producto
const newProduct = await apiClient.createProduct({
  codigo: 'PROD-001',
  nombre: 'Mi Producto',
  precio_venta: 100,
  precio_costo: 50,
})
```

## 📝 Credenciales Demo

```
Email: admin@example.com
Password: admin123
```

## 🎨 Estilos

El proyecto usa **Tailwind CSS** con colores personalizados:

```javascript
primary: {
  600: '#0284c7',    // Azul principal
  700: '#0369a1',
}
```

## 🔄 Flujo de Usuario

1. **Login** (`/login`)
   - Ingresa email y contraseña
   - Recibe JWT tokens

2. **Dashboard** (`/dashboard`)
   - Vista general del inventario
   - Estadísticas rápidas
   - Acciones rápidas

3. **Productos** (`/products`)
   - Listar productos
   - Crear/editar/eliminar

4. **Movimientos** (`/movements`)
   - Historial de entradas/salidas
   - Filtros por tipo

## 🚀 Deployment

### Vercel (Recomendado)

```bash
npm install -g vercel
vercel
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 📚 Recursos

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [Zustand](https://github.com/pmndrs/zustand)
- [API Backend](../Backend/API_ENDPOINTS.md)

## 🐛 Troubleshooting

### Puerto 3000 en uso
```bash
lsof -i :3000
kill -9 <PID>
```

### Errores de CORS
Verificar que `NEXT_PUBLIC_API_URL` apunta al backend correcto

### Token expirado
El frontend intenta refrescar automáticamente, si falla redirige a login

## 📄 Licencia

MIT
