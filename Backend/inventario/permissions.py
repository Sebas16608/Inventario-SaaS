from rest_framework.permissions import BasePermission


class CanCreateProduct(BasePermission):
    """Permiso para crear productos"""
    
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.has_permission('create_product')
        return True


class CanEditProduct(BasePermission):
    """Permiso para editar productos"""
    
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH']:
            return request.user.has_permission('edit_product')
        return True


class CanDeleteProduct(BasePermission):
    """Permiso para eliminar productos"""
    
    def has_permission(self, request, view):
        if request.method in ['DELETE']:
            return request.user.has_permission('delete_product')
        return True


class CanViewProduct(BasePermission):
    """Permiso para ver productos"""
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.has_permission('view_product')
        return True


class CanCreateMovement(BasePermission):
    """Permiso para crear movimientos"""
    
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.has_permission('create_movement')
        return True


class CanEditMovement(BasePermission):
    """Permiso para editar movimientos"""
    
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH']:
            return request.user.has_permission('edit_movement')
        return True


class CanViewReports(BasePermission):
    """Permiso para ver reportes"""
    
    def has_permission(self, request, view):
        return request.user.has_permission('view_reports')
