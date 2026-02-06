# 📦 Inventario-SaaS

**Sistema de Gestión de Inventario Multi-Tenant (SaaS)**

Una plataforma profesional de gestión de inventario construida con Django REST Framework y diseñada para soportar múltiples organizaciones en una única instancia (multi-tenancy).

![Django](https://img.shields.io/badge/Django-6.0-green)
![DRF](https://img.shields.io/badge/DRF-3.16-blue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Características Principales

- **🏢 Multi-Tenancy**: Múltiples empresas en una sola aplicación
- **🔐 Autenticación JWT**: Token-based, segura y moderna
- **📦 Gestión de Inventario**: Categorías, productos, stock y movimientos
- **📊 Auditoría**: Registro de quién realiza cada acción
- **🗄️ API RESTful**: Endpoints completos listos para consumir
- **📝 Documentación Completa**: Código bien documentado
- **⚡ Django ORM**: Base de datos flexible y potente
- **✨ MVP Simplificado**: Modelo de autenticación limpio y eficiente

## 📁 Estructura del Proyecto

```
Inventario-SaaS/
├── Backend/                    # Aplicación Django
│   ├── accounts/              # Gestión de usuarios y organizaciones
│   ├── inventario/            # Gestión de inventario
│   ├── config/                # Configuración de Django
│   ├── utils/                 # Utilities y mixins
│   ├── docs/                  # Documentación y scripts
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md
│   └── db.sqlite3            # Base de datos (desarrollo)
│
├── Frontend/                   # Aplicación Frontend (próximamente)
│
├── CAMBIOS.md                 # Resumen de cambios realizados
├── RESUMEN_FINAL.md          # Resumen del proyecto
└── README.md                  # Este archivo
```

## 🛠️ Stack Tecnológico

### Backend
- **Django 6.0.2**: Framework web Python
- **Django REST Framework**: API REST
- **JWT**: Autenticación stateless
- **PostgreSQL** (producción) / SQLite (desarrollo)
- **CORS Headers**: Comunicación Frontend-Backend
- **Pillow**: Procesamiento de imágenes

### Frontend (Por implementar)
- React / Vue.js
- TypeScript
- Axios / Fetch API
- Tailwind CSS / Material UI

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.9+
- pip
- Git

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/Sebas16608/Inventario-SaaS.git
cd Inventario-SaaS
```

2. **Configurar Backend**
```bash
cd Backend

# Crear virtual environment
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Crear migraciones y base de datos
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

El servidor estará en: **http://localhost:8000**

Admin en: **http://localhost:8000/admin**

## 📊 Modelos de Base de Datos

### Empresa (Tenant)
```python
- nombre: Nombre de la empresa
- nicho: Tipo (farmacia, veterinaria)
- direccion: Dirección física
- telefono: Teléfono de contacto
- email: Email de contacto
- is_active: Estado
- created_at/updated_at: Timestamps
```

### User
```python
- email: Email único
- username: Nombre de usuario
- first_name / last_name: Nombre completo
- telefono: Teléfono personal
- empresa: ForeignKey(Empresa)
- is_active: Estado
- created_at/updated_at: Timestamps
```

### Category
```python
- nombre: Nombre de la categoría
- descripcion: Descripción
- is_active: Estado
```

### Product
```python
- codigo: Código único
- nombre: Nombre del producto
- descripcion: Descripción
- categoria: ForeignKey(Category)
- precio_venta: Precio de venta
- precio_costo: Costo
- is_active: Estado
```

### Movement
```python
- producto: ForeignKey(Product)
- empresa: ForeignKey(Empresa)
- tipo: Entrada/Salida
- cantidad: Cantidad movida
- razon: Motivo del movimiento
- created_at: Fecha del movimiento
```

### Movement
```python
- product: Producto
- movement_type: in, out, adjustment, transfer
- quantity: Cantidad
- status: pending, completed, cancelled
- created_by: Usuario que realizó el movimiento
```

## 🔑 API Endpoints

### Autenticación
```
POST   /api/auth/token/         - Obtener token JWT
POST   /api/auth/token/refresh/ - Refrescar token
```

### Usuarios
```
GET    /api/users/              - Listar usuarios
POST   /api/users/              - Crear usuario
GET    /api/users/{id}/         - Obtener usuario
PUT    /api/users/{id}/         - Actualizar usuario
DELETE /api/users/{id}/         - Eliminar usuario
```

### Productos
```
GET    /api/products/           - Listar productos
POST   /api/products/           - Crear producto
GET    /api/products/{id}/      - Obtener producto detallado
PUT    /api/products/{id}/      - Actualizar producto
DELETE /api/products/{id}/      - Eliminar producto
```

### Stock
```
GET    /api/stock/              - Listar stock
POST   /api/stock/              - Crear/Actualizar stock
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

### Categorías
```
GET    /api/categories/         - Listar categorías
POST   /api/categories/         - Crear categoría
GET    /api/categories/{id}/    - Obtener categoría
PUT    /api/categories/{id}/    - Actualizar categoría
DELETE /api/categories/{id}/    - Eliminar categoría
```

## 🔐 Autenticación

### Obtener Token JWT

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"admin123"}'
```

**Respuesta:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Usar Token en Requests

```bash
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 📚 Roles y Permisos

### Roles Predefinidos

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **Admin** | Administrador de la organización | Todos |
| **Manager** | Gerente de inventario | Crear/editar productos, gestionar stock, ver reportes |
| **Staff** | Personal de almacén | Crear movimientos, ver productos y stock |
| **Viewer** | Visualizador | Solo lectura (productos, stock, reportes) |

### Permisos Disponibles

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

## 🧪 Crear Datos de Prueba

### Inicializar Permisos
```bash
cd Backend
python manage.py shell < docs/init_permissions.py
```

### Crear Datos de Prueba
```bash
python manage.py shell < docs/create_test_data.py
```

Esto creará:
- 1 organización de prueba (Test Company)
- 4 roles con permisos asignados
- 3 usuarios de prueba:
  - admin@test.com (Admin)
  - manager@test.com (Manager)
  - staff@test.com (Staff)

## 📖 Documentación

- **[Backend/README.md](Backend/README.md)** - Documentación técnica del backend
- **[Backend/docs/SETUP.md](Backend/docs/SETUP.md)** - Guía detallada de instalación
- **[CAMBIOS.md](CAMBIOS.md)** - Resumen de cambios en la refactorización
- **[RESUMEN_FINAL.md](RESUMEN_FINAL.md)** - Resumen completo del proyecto

## 🔧 Desarrollo

### Crear Migraciones
```bash
cd Backend
python manage.py makemigrations
python manage.py migrate
```

### Ejecutar Tests
```bash
python manage.py test
```

### Formato de Código
```bash
pip install black flake8
black .
flake8 .
```

## 🚀 Deployment

### Producción con Gunicorn y PostgreSQL

1. **Instalar Gunicorn**
```bash
pip install gunicorn
```

2. **Configurar base de datos PostgreSQL**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=inventario_saas
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
```

3. **Recolectar archivos estáticos**
```bash
python manage.py collectstatic --noinput
```

4. **Ejecutar con Gunicorn**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Variables de Entorno para Producción

```env
DEBUG=False
SECRET_KEY=your-secure-secret-key
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=inventario_saas
DB_USER=postgres
DB_PASSWORD=secure-password
DB_HOST=db.yourdomain.com
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 📈 Roadmap

- [ ] **Fase 1 (Completada)**
  - [x] Estructura SaaS multi-tenant
  - [x] Modelos de base de datos
  - [x] Autenticación JWT
  - [x] Permisos y roles

- [ ] **Fase 2 (Próxima)**
  - [ ] ViewSets para todos los modelos
  - [ ] Configuración de URLs y routers
  - [ ] Tests unitarios
  - [ ] Documentación Swagger

- [ ] **Fase 3**
  - [ ] Reportes avanzados
  - [ ] Gráficos de inventario
  - [ ] Exportación a Excel/PDF
  - [ ] Búsqueda avanzada

- [ ] **Fase 4**
  - [ ] Frontend React
  - [ ] Dashboard interactivo
  - [ ] Notificaciones en tiempo real
  - [ ] Integración con proveedores

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 👥 Autor

**Sebastián Mora**
- GitHub: [@Sebas16608](https://github.com/Sebas16608)
- Email: contacto@ejemplo.com

## 💬 Soporte

Para reportar issues o solicitar features, abre un [issue en GitHub](https://github.com/Sebas16608/Inventario-SaaS/issues).

## 📚 Recursos Útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/docs/)

---

**Última actualización:** 5 de febrero de 2026

**Estado:** ✅ Backend funcional y listo para usar
