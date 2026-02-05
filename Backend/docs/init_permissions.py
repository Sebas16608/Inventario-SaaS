"""
Script para inicializar permisos en la base de datos
Ejecutar con: python manage.py shell < docs/init_permissions.py
"""

from accounts.models import Permission

# Definir todos los permisos del sistema
PERMISSIONS = [
    {
        'code': 'create_product',
        'description': 'Crear nuevos productos'
    },
    {
        'code': 'edit_product',
        'description': 'Editar productos existentes'
    },
    {
        'code': 'delete_product',
        'description': 'Eliminar productos'
    },
    {
        'code': 'view_product',
        'description': 'Ver productos'
    },
    {
        'code': 'create_movement',
        'description': 'Crear movimientos de inventario'
    },
    {
        'code': 'edit_movement',
        'description': 'Editar movimientos de inventario'
    },
    {
        'code': 'delete_movement',
        'description': 'Eliminar movimientos de inventario'
    },
    {
        'code': 'view_movement',
        'description': 'Ver movimientos de inventario'
    },
    {
        'code': 'view_reports',
        'description': 'Ver reportes del sistema'
    },
    {
        'code': 'manage_users',
        'description': 'Gestionar usuarios de la organización'
    },
]

# Crear permisos
for perm_data in PERMISSIONS:
    permission, created = Permission.objects.get_or_create(
        code=perm_data['code'],
        defaults={'description': perm_data['description']}
    )
    status = 'Creado' if created else 'Ya existe'
    print(f"{status}: {permission.code}")

print(f"\n✅ Total permisos: {Permission.objects.count()}")
