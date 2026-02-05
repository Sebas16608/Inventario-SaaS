# Inventario SaaS - Backend

Backend del sistema de gestión de inventario multi-tenant construido con Django REST Framework.

## Características

- ✅ **Multi-Tenancy**: Soporte completo para múltiples organizaciones
- ✅ **Autenticación JWT**: Token-based authentication con refresh tokens
- ✅ **Control de Acceso Granular**: Roles y permisos personalizables
- ✅ **Gestión de Inventario**: Categorías, productos, stock y movimientos
- ✅ **Auditoría**: Registro de quién realiza cada acción
- ✅ **API RESTful**: Endpoints completamente documentados

## Estructura del Proyecto

```
Backend/
├── accounts/              # Gestión de usuarios y organizaciones
│   ├── models.py         # User, Organization, Role, Permission
│   ├── serializers.py    # Serializers para API
│   ├── permissions.py    # Permisos personalizados
│   └── views.py          # ViewSets
├── inventario/           # Gestión de inventario
│   ├── models/           # Category, Product, Stock, Movement
│   ├── serializers/      # Serializers para cada modelo
│   ├── permissions.py    # Permisos específicos de inventario
│   └── views/            # ViewSets y views
├── config/
│   ├── settings/
│   │   ├── base.py       # Configuración base
│   │   ├── development.py # Dev settings
│   │   └── production.py  # Prod settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── utils/                # Utilities comunes
    ├── __init__.py       # TenantModel base
    └── mixins.py         # Mixins para vistas
```

## Instalación

### Requisitos previos
- Python 3.9+
- pip
- virtualenv (recomendado)

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Sebas16608/Inventario-SaaS.git
cd Inventario-SaaS/Backend
```

2. **Crear virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
```

5. **Crear migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## Modelos

### Organization
Representa una empresa/cliente en el sistema SaaS.

```python
- name: str
- slug: str (único)
- description: str
- logo: ImageField
- is_active: bool
- created_at: datetime
- updated_at: datetime
```

### CustomUser
Usuario del sistema vinculado a una organización.

```python
- email: str (único)
- organization: ForeignKey(Organization)
- role: ForeignKey(Role)
- first_name: str
- last_name: str
- is_active: bool
- created_at: datetime
```

### Role
Rol dentro de una organización con permisos asociados.

```python
ROLES:
- admin: Acceso total
- manager: Gestión de inventario
- staff: Personal de almacén
- viewer: Solo lectura
```

### Category
Categoría de productos.

```python
- name: str
- description: str
- is_active: bool
```

### Product
Producto del inventario.

```python
- code: str
- name: str
- sku: str (único)
- category: ForeignKey(Category)
- price: Decimal
- cost: Decimal
- is_active: bool
```

### Stock
Stock de un producto por almacén.

```python
- product: ForeignKey(Product)
- warehouse: str
- quantity: int
- minimum_quantity: int
- maximum_quantity: int
```

### Movement
Movimiento de inventario (entrada/salida).

```python
TIPOS:
- in: Entrada
- out: Salida
- adjustment: Ajuste
- transfer: Transferencia

ESTADOS:
- pending: Pendiente
- completed: Completado
- cancelled: Cancelado
```

## API Endpoints

### Autenticación
```
POST   /api/auth/token/         - Obtener token
POST   /api/auth/token/refresh/  - Refrescar token
```

### Usuarios
```
GET    /api/users/              - Listar usuarios
POST   /api/users/              - Crear usuario
GET    /api/users/{id}/         - Obtener usuario
PUT    /api/users/{id}/         - Actualizar usuario
DELETE /api/users/{id}/         - Eliminar usuario
```

### Organizaciones
```
GET    /api/organizations/      - Listar organizaciones
POST   /api/organizations/      - Crear organización
GET    /api/organizations/{id}/ - Obtener organización
PUT    /api/organizations/{id}/ - Actualizar organización
```

### Productos
```
GET    /api/products/           - Listar productos
POST   /api/products/           - Crear producto
GET    /api/products/{id}/      - Obtener producto
PUT    /api/products/{id}/      - Actualizar producto
DELETE /api/products/{id}/      - Eliminar producto
```

### Stock
```
GET    /api/stock/              - Listar stock
POST   /api/stock/              - Crear stock
GET    /api/stock/{id}/         - Obtener stock
PUT    /api/stock/{id}/         - Actualizar stock
```

### Movimientos
```
GET    /api/movements/          - Listar movimientos
POST   /api/movements/          - Crear movimiento
GET    /api/movements/{id}/     - Obtener movimiento
PUT    /api/movements/{id}/     - Actualizar movimiento
POST   /api/movements/{id}/complete/ - Completar movimiento
```

## Autenticación

El sistema usa **JWT (JSON Web Tokens)** para autenticación.

### Obtener token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'
```

**Respuesta:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Usar token en requests
```bash
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Permisos

### Permisos del Sistema
- `create_product`: Crear productos
- `edit_product`: Editar productos
- `delete_product`: Eliminar productos
- `view_product`: Ver productos
- `create_movement`: Crear movimientos
- `edit_movement`: Editar movimientos
- `delete_movement`: Eliminar movimientos
- `view_movement`: Ver movimientos
- `view_reports`: Ver reportes
- `manage_users`: Gestionar usuarios

### Roles Predefinidos

**Admin**
- Acceso total a todas las operaciones
- Gestionar usuarios y roles
- Ver reportes

**Manager**
- Crear y editar productos
- Gestionar stock y movimientos
- Ver reportes

**Staff**
- Crear movimientos de inventario
- Ver productos y stock

**Viewer**
- Solo lectura de productos y stock

## Desarrollo

### Crear migración
```bash
python manage.py makemigrations
python manage.py migrate
```

### Ejecutar tests
```bash
python manage.py test
```

### Crear usuario de prueba
```bash
python manage.py shell
```

```python
from accounts.models import Organization, CustomUser, Role, Permission
from django.contrib.auth.models import User

# Crear organización
org = Organization.objects.create(
    name="Mi Empresa",
    slug="mi-empresa"
)

# Crear usuario
user = CustomUser.objects.create_user(
    email="admin@example.com",
    password="password123",
    organization=org,
    first_name="Admin",
    last_name="User"
)
```

## Variables de Entorno

Ver `.env.example` para todas las variables disponibles.

### Desarrollo
```env
DEBUG=True
SECRET_KEY=dev-secret-key
DJANGO_SETTINGS_MODULE=config.settings.development
```

### Producción
```env
DEBUG=False
SECRET_KEY=your-secure-secret-key
DJANGO_SETTINGS_MODULE=config.settings.production
DB_ENGINE=django.db.backends.postgresql
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Deployment

### Con Gunicorn y PostgreSQL

1. **Instalar Gunicorn**
```bash
pip install gunicorn
```

2. **Collectar archivos estáticos**
```bash
python manage.py collectstatic --noinput
```

3. **Ejecutar con Gunicorn**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Con Docker

Ver `Dockerfile` para instrucciones de containerización.

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.

## Soporte

Para reportar issues o solicitar features, abre un issue en GitHub.
