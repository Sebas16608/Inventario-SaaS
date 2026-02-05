from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from inventario.models.category import Category
from inventario.serializers import CategorySerializer, ProductSerializer
from utils.mixins import TenantFilterMixin


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías de productos.
    
    Endpoints disponibles:
    - GET /api/categories/ - Listar categorías
    - POST /api/categories/ - Crear categoría
    - GET /api/categories/{id}/ - Detalles de la categoría
    - PUT /api/categories/{id}/ - Actualizar categoría
    - PATCH /api/categories/{id}/ - Actualizar parcialmente
    - DELETE /api/categories/{id}/ - Eliminar categoría
    - GET /api/categories/{id}/products/ - Productos en la categoría
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, TenantFilterMixin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def products(self, request, pk=None):
        """Obtener todos los productos de esta categoría"""
        category = self.get_object()
        products = category.products.all()
        if not request.user.is_superuser:
            products = products.filter(organization=request.user.organization)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def deactivate(self, request, pk=None):
        """Desactivar categoría"""
        category = self.get_object()
        category.is_active = False
        category.save()
        return Response({'message': 'Categoría desactivada'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def activate(self, request, pk=None):
        """Activar categoría"""
        category = self.get_object()
        category.is_active = True
        category.save()
        return Response({'message': 'Categoría activada'})
