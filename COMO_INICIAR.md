# 🚀 Cómo Iniciar Inventario-SaaS

## Requisitos Previos
- ✅ Python 3.8+ con venv activado
- ✅ Node.js 18+ instalado
- ✅ npm/yarn disponible

---

## 🔥 PASO 1: Iniciar Backend (Django)

Abre una **NUEVA TERMINAL** y ejecuta:

```bash
cd /home/sebastian/Proyectos/Inventario-SaaS/Backend
/home/sebastian/Proyectos/Inventario-SaaS/.venv/bin/python manage.py runserver 0.0.0.0:8000
```

Deberías ver:
```
Starting development server at http://0.0.0.0:8000/
```

**Backend URL:** http://localhost:8000/api
**Swagger Docs:** http://localhost:8000/api/docs/

---

## 🎨 PASO 2: Iniciar Frontend (Next.js)

Abre una **SEGUNDA TERMINAL DIFERENTE** y ejecuta:

```bash
cd /home/sebastian/Proyectos/Inventario-SaaS/Frontend
npm run dev
```

Deberías ver:
```
  ▲ Next.js 14.2.35
  - Local:        http://localhost:3000
```

**Frontend URL:** http://localhost:3000

---

## 🔐 PASO 3: Login en la Aplicación

1. Abre http://localhost:3000 en tu navegador
2. Serás redirigido a http://localhost:3000/login automáticamente
3. Usa estas credenciales:
   - **Email:** `admin@example.com`
   - **Password:** `admin123`
4. Click en "Ingresar"

Si ves **"Network Error"**:
- ✅ Verifica que Django esté corriendo en puerto 8000
- ✅ Verifica en DevTools → Network que la request vaya a `http://localhost:8000/api/auth/token/`
- ✅ Asegúrate de que `.env.local` contenga: `NEXT_PUBLIC_API_URL=http://localhost:8000/api`

---

## 📱 URLs Disponibles

| Pantalla | URL | Descripción |
|----------|-----|-------------|
| Login | http://localhost:3000/login | Iniciar sesión |
| Dashboard | http://localhost:3000/dashboard | Panel principal |
| Productos | http://localhost:3000/products | Gestión de productos |
| Nuevo Producto | http://localhost:3000/products/new | Crear producto |
| Movimientos | http://localhost:3000/movements | Historial |
| Nuevo Movimiento | http://localhost:3000/movements/new | Registrar movimiento |

---

## 🔧 Troubleshooting

### Error: "Network Error" en Login

**Solución 1:** Verificar que Django está corriendo
```bash
curl -i http://localhost:8000/api/
# Debe responder con 200 OK o 400
```

**Solución 2:** Verificar la configuración del API URL
```bash
cat Frontend/.env.local
# Debe mostrar: NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**Solución 3:** Revisar DevTools del navegador
- F12 → Console → Buscar errores de CORS
- Network → Ver qué URL está usando para el login

### Error: "Port 8000 already in use"

```bash
# Matar procesos en puerto 8000
pkill -f "manage.py runserver"
# O
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Error: "Port 3000 already in use"

```bash
# El frontend usará 3001 automáticamente
# Pero si quieres matar el proceso:
pkill -f "next dev"
# O
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Error: "ModuleNotFoundError: No module named 'django'"

```bash
# Activar entorno virtual
cd /home/sebastian/Proyectos/Inventario-SaaS
source .venv/bin/activate
# Luego iniciar Django
```

---

## ✨ Características Listas

✅ Login con email  
✅ Dashboard con estadísticas  
✅ Listar productos  
✅ Crear productos  
✅ Listar movimientos  
✅ Crear movimientos  
✅ Responsive design  
✅ Autenticación JWT  

---

## 🎯 Flujo de la Aplicación

```
1. Usuario abre http://localhost:3000
   ↓
2. App redirige a /login (no autenticado)
   ↓
3. Usuario ingresa email y contraseña
   ↓
4. Frontend envía POST a /api/auth/token/
   ↓
5. Backend valida credenciales
   ↓
6. Backend devuelve {access_token, refresh_token}
   ↓
7. Frontend guarda tokens en localStorage
   ↓
8. Frontend redirige a /dashboard
   ↓
9. Todos los requests incluyen Authorization: Bearer <token>
```

---

## 📝 Credenciales Demo

```
Email: admin@example.com
Password: admin123
```

Puedes crear más usuarios desde Django Admin: http://localhost:8000/admin

```
Username: admin
Password: admin
```

---

## 🛑 Para Detener los Servidores

En cada terminal, presiona:
```
Ctrl + C
```

---

¡Listo! Tu aplicación debe estar corriendo correctamente. 🎉
