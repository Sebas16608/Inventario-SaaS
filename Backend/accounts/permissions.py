from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """Solo usuarios autenticados pueden acceder"""
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(BasePermission):
    """Solo admin de la organización"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.role and request.user.role.name == 'admin'


class IsManagerOrAdmin(BasePermission):
    """Manager o admin de la organización"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if request.user.role:
            return request.user.role.name in ['admin', 'manager']
        
        return False


class CanManageUsers(BasePermission):
    """Permiso para gestionar usuarios de la organización"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        return request.user.has_permission('manage_users')
