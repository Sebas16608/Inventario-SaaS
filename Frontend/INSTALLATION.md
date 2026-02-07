# 🚀 Guía de Instalación - Frontend Next.js

## Requisitos Previos

- Node.js 18.17+
- npm o yarn
- Backend ejecutándose en `http://localhost:8000`

## Pasos de Instalación

### 1. Instalar Dependencias

```bash
npm install
```

O con yarn:
```bash
yarn install
```

### 2. Configurar Variables de Entorno

Crear archivo `.env.local`:
```bash
cp .env.example .env.local
```

Contenido del `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 3. Verificar Conectividad con Backend

Asegúrate de que el backend esté ejecutándose:
```bash
# En otra terminal
cd Backend
python manage.py runserver
```

El backend debe estar en: `http://localhost:8000/api`

### 4. Iniciar Servidor de Desarrollo

```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:3000`

## 📋 Checklist de Verificación

- [ ] Node.js instalado (`node --version`)
- [ ] npm instalado (`npm --version`)
- [ ] Backend ejecutándose en `http://localhost:8000`
- [ ] Variables de entorno configuradas (`.env.local`)
- [ ] Dependencias instaladas (`node_modules/`)
- [ ] Servidor de desarrollo iniciado (`npm run dev`)
- [ ] Frontend accesible en `http://localhost:3000`
- [ ] Página de login visible
- [ ] Credenciales demo funcionan (admin@example.com / admin123)

## 🔐 Credenciales Demo

```
Email: admin@example.com
Password: admin123
```

## 🐛 Troubleshooting

### Error: "Cannot find module"
```bash
rm -rf node_modules package-lock.json
npm install
```

### Puerto 3000 en uso
```bash
# Cambiar puerto
npm run dev -- -p 3001
```

### Errores de CORS
- Verificar que `NEXT_PUBLIC_API_URL` es correcto
- Verificar que CORS está habilitado en backend

### Token expirado
- Limpiar localStorage: `localStorage.clear()`
- Recargar página: `F5`

## 📦 Estructura de Carpetas

```
Frontend/
├── src/
│   ├── app/              # Páginas (Next.js 14 App Router)
│   ├── components/       # Componentes reutilizables
│   ├── services/         # Servicios de API
│   ├── store/            # State management
│   ├── types/            # Tipos TypeScript
│   └── globals.css       # Estilos globales
├── public/               # Archivos estáticos
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## 🚀 Comandos Útiles

```bash
# Desarrollo
npm run dev

# Build para producción
npm run build

# Iniciar servidor producción
npm start

# Verificar tipos TypeScript
npm run type-check

# Formatear código
npm run format

# Linting
npm run lint
```

## 🌐 URLs Importantes

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/api`
- Swagger Backend: `http://localhost:8000/api/docs/`
- ReDoc Backend: `http://localhost:8000/api/redoc/`

## 📚 Próximos Pasos

1. [✅] Instalar dependencias
2. [✅] Configurar variables de entorno
3. [✅] Iniciar servidor de desarrollo
4. [ ] Explorar el dashboard
5. [ ] Crear productos
6. [ ] Registrar movimientos
7. [ ] Personalizar según necesidades

## 🎨 Personalización

### Colores

Editar `tailwind.config.ts`:
```typescript
theme: {
  extend: {
    colors: {
      primary: {
        600: '#0284c7',  // Cambiar color principal
      }
    }
  }
}
```

### Componentes

Agregar nuevos componentes en `src/components/`

### Páginas

Agregar nuevas páginas en `src/app/`

## ✨ Listo para Desarrollo

¡El frontend está listo para comenzar! 🎉

Próximo paso: explorar el dashboard en `http://localhost:3000`
