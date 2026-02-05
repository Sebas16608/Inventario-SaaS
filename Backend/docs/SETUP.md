# Guía de Configuración Inicial

## 1. Instalación de Dependencias

```bash
cd Backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configuración de Variables de Entorno

```bash
cp .env.example .env
```

Editar `.env` con tus valores:
```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DJANGO_SETTINGS_MODULE=config.settings.development
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 3. Crear Base de Datos

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Crear Permisos del Sistema

```bash
python manage.py shell < docs/init_permissions.py
```

Esto creará 10 permisos predefinidos que se pueden asignar a roles.

## 5. Crear Datos de Prueba (Opcional)

```bash
python manage.py shell < docs/create_test_data.py
```

Esto creará:
- 1 organización de prueba
- 4 roles (admin, manager, staff, viewer)
- 3 usuarios de prueba

## 6. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

El servidor estará en: http://localhost:8000

## 7. Acceder a Admin

URL: http://localhost:8000/admin

Usa las credenciales del superuser creado o los usuarios de prueba:
- admin@test.com / admin123 (Admin de la organización)
- manager@test.com / manager123 (Manager)
- staff@test.com / staff123 (Staff)

## 8. Probar Autenticación API

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

### Usar el Token en Requests

```bash
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 9. Estructura de Carpetas Importante

```
Backend/
├── config/
│   ├── settings/
│   │   ├── __init__.py      # Settings base
│   │   ├── development.py   # Settings para desarrollo
│   │   └── production.py    # Settings para producción
│   ├── urls.py              # URLs principales (pendiente configuar)
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── accounts/                # Gestión de usuarios
│   ├── models.py            # User, Organization, Role
│   ├── serializers.py       # Serializers
│   └── permissions.py       # Permisos custom
├── inventario/              # Gestión de inventario
│   ├── models/              # Category, Product, Stock, Movement
│   ├── serializers/         # Serializers de inventario
│   └── permissions.py       # Permisos de inventario
├── utils/                   # Utilities
│   ├── __init__.py          # TenantModel base
│   └── mixins.py            # Mixins para multi-tenancy
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## 10. Próximos Pasos

- [ ] Crear ViewSets para cada modelo
- [ ] Configurar URLs de API
- [ ] Implementar documentación Swagger/OpenAPI
- [ ] Crear tests unitarios
- [ ] Configurar logging
- [ ] Implementar rate limiting
- [ ] Crear migraciones iniciales de datos
- [ ] Configurar CI/CD

## 11. Troubleshooting

### Error: "No module named 'rest_framework'"
```bash
pip install djangorestframework
```

### Error: "AUTH_USER_MODEL"
Asegúrate de tener en settings.py:
```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### Error en migraciones
```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

### Error de CORS
Verifica que CORS_ALLOWED_ORIGINS está correctamente configurado en .env

## 12. Comandos Útiles

```bash
# Crear superuser
python manage.py createsuperuser

# Ver migraciones pendientes
python manage.py showmigrations

# Ejecutar migraciones
python manage.py migrate

# Crear app nueva
python manage.py startapp nombre_app

# Limpiar base de datos (solo desarrollo)
python manage.py flush

# Hacer backup de datos
python manage.py dumpdata > backup.json

# Restaurar datos
python manage.py loaddata backup.json

# Shell interactivo de Django
python manage.py shell

# Colectar archivos estáticos (producción)
python manage.py collectstatic --noinput
```

## 13. Variables de Entorno Disponibles

Ver `.env.example` para la lista completa.

## 14. Seguridad

- ✅ Cambiar SECRET_KEY en producción
- ✅ Usar PostgreSQL en producción
- ✅ Configurar HTTPS
- ✅ Usar variables de entorno para secrets
- ✅ Configurar ALLOWED_HOSTS
- ✅ Habilitar SECURE_SSL_REDIRECT
- ✅ Habilitar CSRF protection

---

**¡Sistema listo para empezar!** 🚀
