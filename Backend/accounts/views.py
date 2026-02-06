from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User, Empresa
from .serializers import UserSerializer, EmpresaSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios - MVP Simplificado.
    
    Endpoints disponibles:
    - GET /api/users/ - Listar usuarios
    - POST /api/users/ - Crear usuario
    - GET /api/users/{id}/ - Detalles del usuario
    - PUT /api/users/{id}/ - Actualizar usuario
    - PATCH /api/users/{id}/ - Actualizar parcialmente
    - DELETE /api/users/{id}/ - Eliminar usuario
    - POST /api/users/me/ - Mi perfil
    - POST /api/users/{id}/cambiar-contraseña/ - Cambiar contraseña
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['empresa', 'email', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['email', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Filtrar usuarios por empresa si no es superuser"""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if self.request.user.empresa:
                queryset = queryset.filter(empresa=self.request.user.empresa)
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener mi perfil"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cambiar_contraseña(self, request, pk=None):
        """Cambiar contraseña del usuario"""
        user = self.get_object()
        
        # Solo el usuario puede cambiar su propia contraseña (o superuser)
        if request.user.id != user.id and not request.user.is_superuser:
            return Response(
                {'error': 'No tienes permiso para cambiar la contraseña de otro usuario'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        contraseña_actual = request.data.get('contraseña_actual')
        contraseña_nueva = request.data.get('contraseña_nueva')
        
        if not contraseña_actual or not contraseña_nueva:
            return Response(
                {'error': 'Debes proporcionar contraseña actual y nueva'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(contraseña_actual):
            return Response(
                {'error': 'Contraseña actual incorrecta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(contraseña_nueva)
        user.save()
        return Response({'message': 'Contraseña actualizada correctamente'})


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar empresas - MVP Simplificado.
    
    Endpoints disponibles:
    - GET /api/empresas/ - Listar empresas
    - POST /api/empresas/ - Crear empresa
    - GET /api/empresas/{id}/ - Detalles de la empresa
    - PUT /api/empresas/{id}/ - Actualizar empresa
    - PATCH /api/empresas/{id}/ - Actualizar parcialmente
    - DELETE /api/empresas/{id}/ - Eliminar empresa
    - POST /api/empresas/{id}/desactivar/ - Desactivar empresa
    - POST /api/empresas/{id}/activar/ - Activar empresa
    - GET /api/empresas/me/ - Mi empresa
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nicho', 'is_active']
    search_fields = ['nombre', 'email']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtrar empresas por la del usuario si no es superuser"""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if self.request.user.empresa:
                queryset = queryset.filter(id=self.request.user.empresa.id)
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener información de mi empresa"""
        if not request.user.empresa:
            return Response(
                {'error': 'No perteneces a ninguna empresa'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EmpresaSerializer(request.user.empresa)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def desactivar(self, request, pk=None):
        """Desactivar empresa"""
        empresa = self.get_object()
        empresa.is_active = False
        empresa.save()
        return Response({'message': 'Empresa desactivada'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def activar(self, request, pk=None):
        """Activar empresa"""
        empresa = self.get_object()
        empresa.is_active = True
        empresa.save()
        return Response({'message': 'Empresa activada'})
