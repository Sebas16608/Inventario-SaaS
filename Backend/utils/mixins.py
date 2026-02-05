from django.db.models import QuerySet
from rest_framework.permissions import BasePermission


class TenantFilterMixin:
    """Mixin para filtrar querysets por organización del usuario"""
    
    def get_queryset(self):
        """Filtra el queryset por la organización del usuario"""
        queryset = super().get_queryset()
        
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return queryset
            
            user_organization = self.request.user.organization
            if user_organization:
                return queryset.filter(organization=user_organization)
        
        return queryset.none()


class IsTenantUser(BasePermission):
    """Permiso que verifica que el usuario pertenece a la organización"""
    
    def has_object_permission(self, request, view, obj):
        """Verifica que el usuario está en la misma organización del objeto"""
        if request.user.is_superuser:
            return True
        
        if hasattr(obj, 'organization'):
            return obj.organization == request.user.organization
        
        return False


class IsAdminOrManager(BasePermission):
    """Permiso para admins y managers"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if request.user.role:
            return request.user.role.name in ['admin', 'manager']
        
        return False


class HasPermission(BasePermission):
    """Permiso genérico que verifica un permission_code específico"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Obtener el código de permiso requerido de la vista
        permission_required = getattr(view, 'permission_required', None)
        
        if permission_required is None:
            return True
        
        return request.user.has_permission(permission_required)
