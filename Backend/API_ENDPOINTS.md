# API REST - Inventario SaaS

## 🚀 Estado: 100% OPERATIVO

Tu API REST está completamente funcional y documentada con Swagger.

---

## 📚 Documentación Interactiva

Cuando inicies el servidor, accede a:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **Schema JSON**: `http://localhost:8000/api/schema/`

---

## 🔐 Autenticación

### Obtener Token JWT

```bash
POST /api/auth/token/
Content-Type: application/json

{
  "email": "admin@test.com",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refrescar Token

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar Token en Requests

```bash
GET /api/users/me/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 🎯 Endpoints de Cuenta (Accounts)

### Usuarios

```
GET    /api/users/                    - Listar usuarios (con filtros)
POST   /api/users/                    - Crear usuario
GET    /api/users/{id}/               - Detalles del usuario
PUT    /api/users/{id}/               - Actualizar usuario
PATCH  /api/users/{id}/               - Actualizar parcialmente
DELETE /api/users/{id}/               - Eliminar usuario
GET    /api/users/me/                 - Mi perfil actual
POST   /api/users/{id}/change_password/ - Cambiar contraseña
POST   /api/users/deactivate_account/ - Desactivar mi cuenta
```

**Filtros disponibles:**
- `?organization=<id>` - Por organización
- `?email=<email>` - Por email
- `?is_active=true|false` - Por estado activo
- `?search=<texto>` - Buscar en email, nombre, apellido
- `?ordering=email,-date_joined` - Ordenar resultados

### Organizaciones

```
GET    /api/organizations/            - Listar organizaciones
POST   /api/organizations/            - Crear organización
GET    /api/organizations/{id}/       - Detalles
PUT    /api/organizations/{id}/       - Actualizar
PATCH  /api/organizations/{id}/       - Actualizar parcialmente
DELETE /api/organizations/{id}/       - Eliminar
GET    /api/organizations/me/         - Mi organización
POST   /api/organizations/{id}/deactivate/ - Desactivar
POST   /api/organizations/{id}/activate/   - Activar
```

### Roles

```
GET    /api/roles/                    - Listar roles
POST   /api/roles/                    - Crear rol
GET    /api/roles/{id}/               - Detalles
PUT    /api/roles/{id}/               - Actualizar
PATCH  /api/roles/{id}/               - Actualizar parcialmente
DELETE /api/roles/{id}/               - Eliminar rol
```

### Permisos

```
GET    /api/permissions/              - Listar todos los permisos
GET    /api/permissions/{id}/         - Detalles del permiso
```

---

## 📦 Endpoints de Inventario

### Categorías

```
GET    /api/categories/               - Listar categorías
POST   /api/categories/               - Crear categoría
GET    /api/categories/{id}/          - Detalles
PUT    /api/categories/{id}/          - Actualizar
PATCH  /api/categories/{id}/          - Actualizar parcialmente
DELETE /api/categories/{id}/          - Eliminar
GET    /api/categories/{id}/products/ - Productos en categoría
POST   /api/categories/{id}/deactivate/ - Desactivar
POST   /api/categories/{id}/activate/   - Activar
```

### Productos

```
GET    /api/products/                 - Listar productos
POST   /api/products/                 - Crear producto
GET    /api/products/{id}/            - Detalles
PUT    /api/products/{id}/            - Actualizar
PATCH  /api/products/{id}/            - Actualizar parcialmente
DELETE /api/products/{id}/            - Eliminar
GET    /api/products/{id}/stock/      - Stock del producto
GET    /api/products/low_stock/       - Productos con stock bajo
POST   /api/products/{id}/deactivate/ - Desactivar
POST   /api/products/{id}/activate/   - Activar
```

**Filtros:**
- `?category=<id>` - Por categoría
- `?search=name,code,sku` - Búsqueda avanzada
- `?ordering=price,-created_at` - Ordenamiento

### Stock

```
GET    /api/stock/                    - Listar registros de stock
POST   /api/stock/                    - Crear registro
GET    /api/stock/{id}/               - Detalles
PUT    /api/stock/{id}/               - Actualizar
PATCH  /api/stock/{id}/               - Actualizar parcialmente
DELETE /api/stock/{id}/               - Eliminar
GET    /api/stock/alerts/             - Stock con alertas
GET    /api/stock/summary/            - Resumen por almacén
```

### Movimientos

```
GET    /api/movements/                - Listar movimientos
POST   /api/movements/                - Registrar movimiento
GET    /api/movements/{id}/           - Detalles
PUT    /api/movements/{id}/           - Actualizar
PATCH  /api/movements/{id}/           - Actualizar parcialmente
DELETE /api/movements/{id}/           - Eliminar
GET    /api/movements/by_type/        - Por tipo (IN, OUT, ADJUSTMENT, TRANSFER)
GET    /api/movements/audit/          - Historial de auditoría
GET    /api/movements/summary/        - Resumen de movimientos
POST   /api/movements/{id}/reverse/   - Revertir movimiento
```

---

## 📊 Ejemplos de Uso

### Crear Producto

```bash
POST /api/products/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Laptop Dell",
  "code": "LAPTOP-001",
  "sku": "SKU-12345",
  "description": "Laptop profesional",
  "category": 1,
  "price": 1200.00,
  "cost": 800.00
}
```

### Registrar Movimiento de Entrada

```bash
POST /api/movements/
Authorization: Bearer <token>
Content-Type: application/json

{
  "product": 1,
  "movement_type": "IN",
  "warehouse": "Principal",
  "quantity": 10,
  "reason": "Compra",
  "notes": "Orden de compra #12345"
}
```

### Filtrar Productos Baratos

```bash
GET /api/products/?search=monitor&ordering=price
Authorization: Bearer <token>
```

---

## ✨ Características de la API

✅ **Autenticación JWT** - Tokens seguros con refresh automático  
✅ **Multi-tenancy** - Datos aislados por organización  
✅ **Filtros avanzados** - DjangoFilterBackend integrado  
✅ **Búsqueda completa** - En múltiples campos  
✅ **Paginación** - 20 items por página (configurable)  
✅ **Ordenamiento** - Ordenar por cualquier campo  
✅ **Documentación Swagger** - Interfaz interactiva  
✅ **ReDoc** - Documentación alternativa profesional  
✅ **Permisos granulares** - Control de acceso por rol  
✅ **Auditoría** - Historial completo de movimientos  

---

## 🔒 Seguridad

- JWT con expiración (1 hora)
- Refresh tokens (7 días)
- CORS configurado
- Multi-tenancy obligatorio
- Control de acceso basado en roles (RBAC)
- Tokens rotados automáticamente

---

## 📈 Escalabilidad

- DefaultRouter de DRF para gestión automática
- Paginación configurable
- Filtros optimizados con Django ORM
- Búsqueda en índices
- Ready para cache (Redis)
- Ready para base de datos PostgreSQL

---

## 🚀 Próximos Pasos

1. **Iniciar servidor**: `python Backend/manage.py runserver`
2. **Obtener token**: Acceder a `/api/auth/token/`
3. **Explorar Swagger**: Ir a `/api/docs/`
4. **Crear datos**: Usar la interfaz para crear productos, categorías, etc.
5. **Integrar Frontend**: El Frontend puede consumir los endpoints

---

## 📝 Notas Importantes

- La API filtra automáticamente por organización del usuario
- Los superusuarios ven todos los datos
- Los usuarios normales solo ven datos de su organización
- El stock se actualiza automáticamente con cada movimiento
- Los campos `created_by` y `updated_by` se asignan automáticamente

---

**API completamente operativa y lista para producción.** 🎉
