# Guía de Solución de Problemas - Inventario SaaS

## Cambios Realizados para Arreglar los Errores

### 1. **Error 404 en Productos y Movimientos**

**Causa:** El frontend no podía acceder a los endpoints de productos y movimientos.

**Solución:**
- ✅ Verificado que los endpoints están correctamente registrados en Django
- ✅ Verificado que la autenticación JWT está funcionando
- ✅ Mejorado el manejo de errores en el store de autenticación

### 2. **Error 401 al Crear Productos**

**Causa:** El token JWT no se estaba enviando correctamente con cada request.

**Solución:**
- ✅ Mejorado el interceptor de axios para enviar el token Bearer en cada request
- ✅ Agregado logging para diagnosticar problemas de autenticación
- ✅ Mejorado el manejo de errores 401 con reintentos de autenticación

### 3. **Autenticación con Email (No Username)**

**Problema:** SimpleJWT por defecto usa `username` pero necesitábamos usar `email`.

**Solución:**
- ✅ Creado `CustomTokenObtainPairView` en `Backend/accounts/authentication.py`
- ✅ Customizado el serializador `CustomTokenObtainPairSerializer` para aceptar email
- ✅ Actualizado `config/urls.py` para usar la vista customizada

## Archivos Modificados

### Backend
```
Backend/accounts/authentication.py         [NUEVO] - Custom JWT auth views
Backend/config/urls.py                     [MODIFICADO] - Usar custom auth view
```

### Frontend
```
Frontend/src/store/auth.ts                 [MODIFICADO] - Mejorado checkAuth y login
Frontend/src/app/products/new/page.tsx     [NUEVO] - Página para crear productos
Frontend/src/app/movements/new/page.tsx    [NUEVO] - Página para crear movimientos
Frontend/src/app/movements/page.tsx        [MODIFICADO] - Agregado botón de nuevo movimiento
```

## Prueba del Sistema Completo

### Paso 1: Iniciar el Backend

```bash
cd /home/sebastian/Proyectos/Inventario-SaaS
source .venv/bin/activate    # En Windows: .venv\Scripts\activate
cd Backend
python manage.py runserver
```

El servidor debería estar en: `http://localhost:8000`

### Paso 2: Iniciar el Frontend (en otra terminal)

```bash
cd /home/sebastian/Proyectos/Inventario-SaaS/Frontend
npm run dev
```

El servidor debería estar en: `http://localhost:3000`

### Paso 3: Probar el Login

1. Abre `http://localhost:3000` en tu navegador
2. Automáticamente irá a `http://localhost:3000/login`
3. Usa estas credenciales:
   - **Email:** `admin@example.com`
   - **Password:** `admin123`
4. Deberías ser redirigido a `/dashboard`

### Paso 4: Probar la Navegación

- ✅ **Dashboard:** Deberías ver estadísticas de productos, movimientos y usuarios
- ✅ **Productos:** Deberías ver una lista de productos (aunque esté vacía)
  - Click en "Nuevo Producto" te lleva a `/products/new`
  - Rellena el formulario y guarda
- ✅ **Movimientos:** Deberías ver el historial de movimientos
  - Click en "Nuevo Movimiento" te lleva a `/movements/new`
  - Registra un movimiento de entrada/salida

## URLs Importantes

| Componente | URL | Descripción |
|-----------|-----|-------------|
| Frontend | http://localhost:3000 | Aplicación principal |
| Login | http://localhost:3000/login | Página de login |
| Dashboard | http://localhost:3000/dashboard | Panel principal |
| Productos | http://localhost:3000/products | Gestión de productos |
| Crear Producto | http://localhost:3000/products/new | Crear nuevo producto |
| Movimientos | http://localhost:3000/movements | Historial de movimientos |
| Crear Movimiento | http://localhost:3000/movements/new | Registrar movimiento |
| Backend API | http://localhost:8000/api | API REST |
| Swagger Docs | http://localhost:8000/api/docs | Documentación interactiva |

## Endpoints API Disponibles

### Autenticación
```
POST /api/auth/token/          - Login (email + password)
POST /api/auth/token/refresh/  - Refrescar token
```

### Usuarios
```
GET    /api/users/             - Listar usuarios
POST   /api/users/             - Crear usuario
GET    /api/users/{id}/        - Obtener usuario
PUT    /api/users/{id}/        - Actualizar usuario
GET    /api/users/me/          - Mi perfil
```

### Empresas
```
GET    /api/empresas/          - Listar empresas
POST   /api/empresas/          - Crear empresa
GET    /api/empresas/{id}/     - Obtener empresa
PUT    /api/empresas/{id}/     - Actualizar empresa
```

### Productos
```
GET    /api/products/          - Listar productos
POST   /api/products/          - Crear producto
GET    /api/products/{id}/     - Obtener producto
PUT    /api/products/{id}/     - Actualizar producto
DELETE /api/products/{id}/     - Eliminar producto
```

### Movimientos
```
GET    /api/movements/         - Listar movimientos
POST   /api/movements/         - Crear movimiento
GET    /api/movements/{id}/    - Obtener movimiento
```

### Categorías
```
GET    /api/categories/        - Listar categorías
POST   /api/categories/        - Crear categoría
```

## Solución de Problemas

### Error: "Cannot find module..."
```bash
cd Frontend
npm install
```

### Error: "Connection refused" en puerto 8000
```bash
# El servidor Django no está corriendo
# Ejecuta desde una terminal nueva
cd Backend
python manage.py runserver
```

### Error: "Connection refused" en puerto 3000
```bash
# El servidor Next.js no está corriendo
# Ejecuta desde una terminal nueva
cd Frontend
npm run dev
```

### Error: "404 Not Found" en productos/movimientos
1. Verifica que el token se envía correctamente:
   - Abre DevTools (F12) → Network
   - Busca requests a `/api/products/`
   - Verifica que tengan header: `Authorization: Bearer <token>`
2. Verifica que la sesión está activa:
   - Abre DevTools → Application → LocalStorage
   - Verifica que exista `access_token`

### Error: "Contraseña incorrecta" al login
- Email debe ser exactamente: `admin@example.com`
- Contraseña debe ser exactamente: `admin123`

## Flujo de Autenticación

```
Frontend (Login)
    ↓
[email + password] → POST /api/auth/token/
    ↓
Backend (CustomTokenObtainPairView)
    ↓
Verifica usuario por email
    ↓
Devuelve {access, refresh} tokens
    ↓
Frontend guarda tokens en localStorage
    ↓
Todos los requests posteriores incluyen: Authorization: Bearer <access>
    ↓
Si error 401: intenta refrescar token o redirige a login
```

## Características Implementadas

### ✅ Completado
- [x] Autenticación JWT con email
- [x] Login y logout
- [x] Rutas protegidas
- [x] Dashboard con estadísticas
- [x] Listar productos
- [x] Crear productos
- [x] Listar movimientos
- [x] Crear movimientos
- [x] Responsive design
- [x] Manejo de errores

### ⏳ Por Hacer (Opcional)
- [ ] Editar productos
- [ ] Eliminar productos
- [ ] Buscar y filtrar
- [ ] Paginación
- [ ] Exportar a Excel
- [ ] Dark mode
- [ ] Notificaciones push

## Notas Importantes

1. **JWT Token Lifetime:** Los tokens expiran después de 1 hora (configurable en settings)
2. **Database:** Se usa SQLite en desarrollo (database.db)
3. **Admin Django:** Disponible en http://localhost:8000/admin (admin/admin)
4. **Cambios en Código:** Si modificas el backend, Django reinicia automáticamente
5. **Cambios en Frontend:** Si modificas el frontend, Next.js recarga automáticamente (HMR)

## Contacto y Soporte

Si necesitas ayuda con:
- Errores en el login: Verifica las credenciales en el archivo
- Errores de CORS: Verifica CORS_ALLOWED_ORIGINS en settings
- Problemas de base de datos: Ejecuta `python manage.py migrate`
- Problemas de dependencias: Ejecuta `npm install` o `pip install -r requirements.txt`

¡Listo! Ahora puedes probar tu aplicación Inventario SaaS completamente funcional.
