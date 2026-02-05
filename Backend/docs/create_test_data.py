"""
Script para crear una organización de prueba con usuarios
Ejecutar con: python manage.py shell < docs/create_test_data.py
"""

from accounts.models import Organization, CustomUser, Role, Permission

# Crear organización
org, org_created = Organization.objects.get_or_create(
    slug='test-company',
    defaults={
        'name': 'Test Company',
        'description': 'Organización de prueba'
    }
)
print(f"{'Creada' if org_created else 'Ya existe'}: {org.name}")

# Obtener todos los permisos
all_permissions = Permission.objects.all()
print(f"\nPermisos disponibles: {all_permissions.count()}")

# Crear rol Admin
admin_role, admin_created = Role.objects.get_or_create(
    organization=org,
    name='admin',
    defaults={
        'description': 'Administrador de la organización'
    }
)
if admin_created:
    admin_role.permissions.set(all_permissions)
    print(f"Creado rol: {admin_role.get_name_display()}")
else:
    print(f"Ya existe rol: {admin_role.get_name_display()}")

# Crear rol Manager
manager_role, manager_created = Role.objects.get_or_create(
    organization=org,
    name='manager',
    defaults={
        'description': 'Gerente de inventario'
    }
)
if manager_created:
    manager_perms = all_permissions.exclude(code__in=['manage_users', 'delete_product'])
    manager_role.permissions.set(manager_perms)
    print(f"Creado rol: {manager_role.get_name_display()}")
else:
    print(f"Ya existe rol: {manager_role.get_name_display()}")

# Crear rol Staff
staff_role, staff_created = Role.objects.get_or_create(
    organization=org,
    name='staff',
    defaults={
        'description': 'Personal de almacén'
    }
)
if staff_created:
    staff_perms = all_permissions.filter(code__in=['create_movement', 'view_product', 'view_movement'])
    staff_role.permissions.set(staff_perms)
    print(f"Creado rol: {staff_role.get_name_display()}")
else:
    print(f"Ya existe rol: {staff_role.get_name_display()}")

# Crear rol Viewer
viewer_role, viewer_created = Role.objects.get_or_create(
    organization=org,
    name='viewer',
    defaults={
        'description': 'Solo lectura'
    }
)
if viewer_created:
    viewer_perms = all_permissions.filter(code__in=['view_product', 'view_movement', 'view_reports'])
    viewer_role.permissions.set(viewer_perms)
    print(f"Creado rol: {viewer_role.get_name_display()}")
else:
    print(f"Ya existe rol: {viewer_role.get_name_display()}")

# Crear usuario Admin
admin_user, admin_user_created = CustomUser.objects.get_or_create(
    email='admin@test.com',
    defaults={
        'username': 'admin_test',
        'first_name': 'Admin',
        'last_name': 'Usuario',
        'organization': org,
        'role': admin_role,
        'is_staff': True
    }
)
if admin_user_created:
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"\n✅ Creado usuario admin: {admin_user.email}")
else:
    print(f"\n✅ Ya existe usuario admin: {admin_user.email}")

# Crear usuario Manager
manager_user, manager_user_created = CustomUser.objects.get_or_create(
    email='manager@test.com',
    defaults={
        'username': 'manager_test',
        'first_name': 'Manager',
        'last_name': 'Usuario',
        'organization': org,
        'role': manager_role
    }
)
if manager_user_created:
    manager_user.set_password('manager123')
    manager_user.save()
    print(f"✅ Creado usuario manager: {manager_user.email}")
else:
    print(f"✅ Ya existe usuario manager: {manager_user.email}")

# Crear usuario Staff
staff_user, staff_user_created = CustomUser.objects.get_or_create(
    email='staff@test.com',
    defaults={
        'username': 'staff_test',
        'first_name': 'Staff',
        'last_name': 'Usuario',
        'organization': org,
        'role': staff_role
    }
)
if staff_user_created:
    staff_user.set_password('staff123')
    staff_user.save()
    print(f"✅ Creado usuario staff: {staff_user.email}")
else:
    print(f"✅ Ya existe usuario staff: {staff_user.email}")

print(f"""
═══════════════════════════════════════════════════════════
Datos de prueba creados exitosamente
═══════════════════════════════════════════════════════════

Organización: {org.name}

Usuarios de prueba:
- Email: admin@test.com / Contraseña: admin123 (Rol: Admin)
- Email: manager@test.com / Contraseña: manager123 (Rol: Manager)
- Email: staff@test.com / Contraseña: staff123 (Rol: Staff)

Prueba la autenticación:
curl -X POST http://localhost:8000/api/auth/token/ \\
  -H "Content-Type: application/json" \\
  -d '{{"email":"admin@test.com","password":"admin123"}}'
═══════════════════════════════════════════════════════════
""")
