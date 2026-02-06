"""
Permisos personalizados para el control de acceso en inventario.
"""
from rest_framework import permissions


class IsManagerOrAdmin(permissions.BasePermission):
    """Permiso para gerentes y administradores de la empresa"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Los superusers siempre tienen permiso
        if request.user.is_superuser:
            return True
        
        # Los usuarios con rol admin o manager en su empresa tienen permiso
        if hasattr(request.user, 'role') and request.user.role:
            return request.user.role.nombre in ['admin', 'manager']
        
        return False


class IsEmpresaOwner(permissions.BasePermission):
    """Permiso que verifica que el usuario pertenece a la empresa del objeto"""
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Los superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
        
        # Verificar que el objeto pertenece a la empresa del usuario
        if hasattr(obj, 'empresa'):
            return obj.empresa == request.user.empresa
        
        return False


class CanCreateProduct(permissions.BasePermission):
    """Permiso para crear productos"""
    
    def has_permission(self, request, view):
        if request.method not in ['POST']:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_permission('create_product') or \
               (hasattr(request.user, 'role') and 
                request.user.role and 
                request.user.role.nombre in ['admin', 'manager'])


class CanEditProduct(permissions.BasePermission):
    """Permiso para editar productos"""
    
    def has_permission(self, request, view):
        if request.method not in ['PUT', 'PATCH']:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_permission('edit_product') or \
               (hasattr(request.user, 'role') and 
                request.user.role and 
                request.user.role.nombre in ['admin', 'manager'])
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Verificar que pertenece a la misma empresa
        if hasattr(obj, 'empresa'):
            return obj.empresa == request.user.empresa
        
        return False


class CanDeleteProduct(permissions.BasePermission):
    """Permiso para eliminar productos (solo administradores)"""
    
    def has_permission(self, request, view):
        if request.method not in ['DELETE']:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_permission('delete_product') or \
               (hasattr(request.user, 'role') and 
                request.user.role and 
                request.user.role.nombre == 'admin')
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Solo administradores pueden eliminar
        if hasattr(request.user, 'role') and request.user.role:
            if request.user.role.nombre == 'admin' and \
               hasattr(obj, 'empresa') and \
               obj.empresa == request.user.empresa:
                return True
        
        return False


class CanCreateMovement(permissions.BasePermission):
    """Permiso para crear movimientos de inventario"""
    
    def has_permission(self, request, view):
        if request.method not in ['POST']:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_permission('create_movement') or \
               (hasattr(request.user, 'role') and 
                request.user.role and 
                request.user.role.nombre in ['admin', 'manager', 'staff'])


class CanEditMovement(permissions.BasePermission):
    """Permiso para editar movimientos"""
    
    def has_permission(self, request, view):
        if request.method not in ['PUT', 'PATCH']:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_permission('edit_movement') or \
               (hasattr(request.user, 'role') and 
                request.user.role and 
                request.user.role.nombre in ['admin', 'manager'])
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if hasattr(obj, 'empresa'):
            return obj.empresa == request.user.empresa
        
        return False


class CanViewReports(permissions.BasePermission):
    """Permiso para ver reportes de inventario"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_permission('view_reports') or \
               (hasattr(request.user, 'role') and 
                request.user.role and 
                request.user.role.nombre in ['admin', 'manager', 'viewer'])
