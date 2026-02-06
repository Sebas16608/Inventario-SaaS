from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import CustomUser, Empresa, Role, Permission
from .serializers import (
    CustomUserSerializer,
    EmpresaSerializer,
    RoleSerializer,
    PermissionSerializer,
    CustomUserDetailSerializer,
)
from .permissions import IsManagerOrAdmin
from utils.mixins import TenantFilterMixin


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    
    Endpoints disponibles:
    - GET /api/users/ - Listar usuarios
    - POST /api/users/ - Crear usuario
    - GET /api/users/{id}/ - Detalles del usuario
    - PUT /api/users/{id}/ - Actualizar usuario
    - PATCH /api/users/{id}/ - Actualizar parcialmente
    - DELETE /api/users/{id}/ - Eliminar usuario
    - POST /api/users/change_password/ - Cambiar contraseña
    - GET /api/users/me/ - Mi perfil
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, TenantFilterMixin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization', 'email', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['email', 'date_joined', 'last_login']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomUserDetailSerializer
        return CustomUserSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrar por organización del usuario actual
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = CustomUserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """Cambiar contraseña del usuario"""
        user = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Contraseña antigua incorrecta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Contraseña actualizada correctamente'})
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def deactivate_account(self, request):
        """Desactivar cuenta del usuario"""
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'Cuenta desactivada'})


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar empresas (multi-nicho).
    
    Endpoints disponibles:
    - GET /api/organizations/ - Listar empresas
    - POST /api/organizations/ - Crear empresa
    - GET /api/organizations/{id}/ - Detalles de la empresa
    - PUT /api/organizations/{id}/ - Actualizar empresa
    - PATCH /api/organizations/{id}/ - Actualizar parcialmente
    - DELETE /api/organizations/{id}/ - Eliminar empresa
    - GET /api/organizations/me/ - Mi empresa
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'nicho']
    search_fields = ['nombre', 'slug']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            # Los usuarios normales solo ven su empresa
            queryset = queryset.filter(id=self.request.user.empresa.id)
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener información de mi empresa"""
        empresa = request.user.empresa
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsManagerOrAdmin])
    def deactivate(self, request, pk=None):
        """Desactivar empresa"""
        empresa = self.get_object()
        empresa.is_active = False
        empresa.save()
        return Response({'message': 'Empresa desactivada'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsManagerOrAdmin])
    def activate(self, request, pk=None):
        """Activar empresa"""
        empresa = self.get_object()
        empresa.is_active = True
        empresa.save()
        return Response({'message': 'Empresa activada'})


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar roles y control de acceso.
    
    Endpoints disponibles:
    - GET /api/roles/ - Listar roles
    - POST /api/roles/ - Crear rol
    - GET /api/roles/{id}/ - Detalles del rol
    - PUT /api/roles/{id}/ - Actualizar rol
    - PATCH /api/roles/{id}/ - Actualizar parcialmente
    - DELETE /api/roles/{id}/ - Eliminar rol
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization', 'is_default']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar permisos disponibles (solo lectura).
    
    Endpoints disponibles:
    - GET /api/permissions/ - Listar todos los permisos
    - GET /api/permissions/{id}/ - Detalles del permiso
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['module', 'action']
    search_fields = ['name', 'description', 'module']
    ordering_fields = ['module', 'name']
    ordering = ['module', 'name']
