# ⚡ Guía Rápida de Referencia - Inventario-SaaS MVP

**Para consulta rápida - 1 página**

---

## 🚀 Inicio Rápido (5 minutos)

```bash
# 1. Clonar y entrar
cd Backend

# 2. Virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migraciones (ya hechas)
python manage.py migrate

# 5. Crear admin
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver

# 7. Acceder
# Admin: http://localhost:8000/admin
# API Docs: http://localhost:8000/api/docs/
```

---

## 🔑 API Authentication

```bash
# Obtener token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}'

# Respuesta
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Usar token
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer {access_token}"
```

---

## 📊 Modelos de Datos

### User
```
email, username, first_name, last_name, telefono, empresa (FK)
```

### Empresa
```
nombre, nicho (farmacia|veterinaria), direccion, telefono, email
```

### Category
```
nombre, descripcion
```

### Product
```
codigo, nombre, descripcion, categoria (FK), precio_venta, precio_costo
```

### Movement
```
producto (FK), empresa (FK), tipo (ENTRADA|SALIDA), cantidad, razon
```

---

## 🔗 Endpoints Principales

| Método | URL | Descripción |
|--------|-----|------------|
| GET | `/api/users/` | Listar usuarios |
| POST | `/api/users/` | Crear usuario |
| GET | `/api/users/me/` | Mi perfil |
| GET | `/api/empresas/` | Listar empresas |
| POST | `/api/empresas/` | Crear empresa |
| GET | `/api/empresas/me/` | Mi empresa |
| GET | `/api/products/` | Listar productos |
| POST | `/api/products/` | Crear producto |
| GET | `/api/movements/` | Listar movimientos |
| POST | `/api/movements/` | Registrar movimiento |
| GET | `/api/categories/` | Listar categorías |

---

## 🛠️ Comandos Django Útiles

```bash
# Crear superuser
python manage.py createsuperuser

# Crear app
python manage.py startapp app_name

# Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# Shell Django interactivo
python manage.py shell

# Ver usuarios/empresas en shell
python manage.py shell
>>> from accounts.models import User, Empresa
>>> User.objects.all()
>>> Empresa.objects.all()

# Limpiar BD (SOLO DESARROLLO)
python manage.py flush

# Validar código
python manage.py check

# Recolectar estáticos (PRODUCCIÓN)
python manage.py collectstatic --noinput
```

---

## 📁 Estructura Importante

```
Backend/
├── accounts/
│   ├── models.py          ← User, Empresa
│   ├── views.py           ← UserViewSet, EmpresaViewSet
│   ├── serializers.py     ← Serializers
│   └── admin.py           ← Admin site
├── inventario/
│   ├── models/            ← Category, Product, Movement
│   ├── serializers/       ← Serializers
│   └── views/             ← ViewSets
├── config/
│   ├── settings.py        ← Configuración
│   ├── urls.py            ← URLs
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

---

## 🔐 Datos de Prueba

```
Superuser:
  Email: admin@example.com
  Password: admin123

Empresa demo:
  Nombre: Farmacia Central
  Nicho: farmacia

Usuario demo:
  Email: gerente@example.com
  Empresa: Farmacia Central
```

---

## 📚 Documentación

| Archivo | Contenido |
|---------|----------|
| [README.md](README.md) | Visión general |
| [RESUMEN_MVP.md](RESUMEN_MVP.md) | Estado del proyecto |
| [Backend/API_ENDPOINTS.md](Backend/API_ENDPOINTS.md) | API completa |
| [Backend/docs/SETUP.md](Backend/docs/SETUP.md) | Setup detallado |
| [DOCUMENTACION_INDICE.md](DOCUMENTACION_INDICE.md) | Índice de docs |

---

## 🌐 URLs Locales

```
Admin: http://localhost:8000/admin
Swagger: http://localhost:8000/api/docs/
ReDoc: http://localhost:8000/api/redoc/
API Root: http://localhost:8000/api/
```

---

## 🚨 Troubleshooting Común

### Error: "ModuleNotFoundError: No module named 'django'"
```bash
pip install -r requirements.txt
```

### Error: "database is locked"
```bash
rm db.sqlite3
python manage.py migrate
```

### Error: "Migraciones pendientes"
```bash
python manage.py migrate
```

### Error: CORS
- Check `CORS_ALLOWED_ORIGINS` en settings.py
- Debe incluir tu frontend URL

---

## 💾 Variables de Entorno (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=config.settings.development
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

## 📈 Ejemplo Completo: Crear Producto

```bash
# 1. Obtener token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' \
  | jq -r '.access')

# 2. Crear categoría
curl -X POST http://localhost:8000/api/categories/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Medicamentos","descripcion":"Medicamentos en general"}'

# 3. Crear producto
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo":"PROD-001",
    "nombre":"Paracetamol",
    "descripcion":"Analgésico",
    "categoria":1,
    "precio_venta":5.50,
    "precio_costo":3.00
  }'

# 4. Listar productos
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔄 Workflow Típico

1. **Obtener token** → POST `/api/auth/token/`
2. **Crear empresa** → POST `/api/empresas/`
3. **Crear usuario** → POST `/api/users/`
4. **Crear categoría** → POST `/api/categories/`
5. **Crear producto** → POST `/api/products/`
6. **Registrar movimiento** → POST `/api/movements/`

---

## ✅ Checklist de Desarrollo

- [ ] Backend funcionando (`python manage.py runserver`)
- [ ] Swagger accesible (`/api/docs/`)
- [ ] Token obtenible (`/api/auth/token/`)
- [ ] Crear usuario funciona
- [ ] Crear empresa funciona
- [ ] Crear producto funciona
- [ ] Registrar movimiento funciona
- [ ] Admin accesible

---

## 🎯 Status Actual

✅ MVP Completado  
✅ API Funcional  
✅ Documentación Completa  
✅ Base de Datos Migrada  

**Listo para:** Frontend Development

---

## 📞 Ayuda Rápida

**¿Cómo obtener un token?**  
→ `curl -X POST http://localhost:8000/api/auth/token/` con email y password

**¿Cómo ver mi perfil?**  
→ `GET /api/users/me/` (requiere token)

**¿Cuáles son los endpoints?**  
→ `http://localhost:8000/api/docs/` (Swagger)

**¿Hay datos de prueba?**  
→ Sí, mira "Datos de Prueba" arriba

**¿Dónde está la documentación?**  
→ [DOCUMENTACION_INDICE.md](DOCUMENTACION_INDICE.md)

---

## 🚀 Deploy a Producción

```bash
# 1. Cambiar DEBUG=False en settings.py
# 2. Configurar ALLOWED_HOSTS
# 3. Usar PostgreSQL en lugar de SQLite
# 4. Configurar email settings
# 5. Generar SECRET_KEY fuerte
# 6. Configurar HTTPS
# 7. Usar Gunicorn/uWSGI
# 8. Configurar reverse proxy (Nginx)
```

---

**Guía rápida de Inventario-SaaS MVP**  
**Versión:** 1.0.0  
**Última actualización:** 6 Febrero 2026
