from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models

from inventario.models.product import Product
from inventario.serializers import ProductSerializer, ProductDetailSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos del inventario.
    
    Endpoints disponibles:
    - GET /api/products/ - Listar productos
    - POST /api/products/ - Crear producto
    - GET /api/products/{id}/ - Detalles del producto
    - PUT /api/products/{id}/ - Actualizar producto
    - PATCH /api/products/{id}/ - Actualizar parcialmente
    - DELETE /api/products/{id}/ - Eliminar producto
    - GET /api/products/{id}/bajo-stock/ - Productos con stock bajo
    - POST /api/products/{id}/desactivar/ - Desactivar producto
    - POST /api/products/{id}/activar/ - Activar producto
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['empresa', 'categoria', 'is_active']
    search_fields = ['nombre', 'proveedor']
    ordering_fields = ['nombre', 'precio_venta', 'cantidad', 'created_at']
    ordering = ['nombre']
    
    def get_queryset(self):
        """Filtrar productos por empresa del usuario autenticado"""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if self.request.user.empresa:
                queryset = queryset.filter(empresa=self.request.user.empresa)
        return queryset
    
    def get_serializer_class(self):
        """Usar serializador detallado para retrieve"""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
    
    def perform_create(self, serializer):
        """Asignar la empresa del usuario al crear producto"""
        if self.request.user.empresa:
            serializer.save(empresa=self.request.user.empresa)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def bajo_stock(self, request):
        """Obtener productos con stock bajo (menor que stock_minimo)"""
        queryset = self.get_queryset()
        products = queryset.filter(cantidad__lt=models.F('stock_minimo')).distinct()
        
        serializer = self.get_serializer_class()(products, many=True)
        return Response({
            'count': products.count(),
            'resultados': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def desactivar(self, request, pk=None):
        """Desactivar producto"""
        product = self.get_object()
        product.is_active = False
        product.save()
        return Response({
            'message': 'Producto desactivado',
            'producto_id': product.id,
            'nombre': product.nombre
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def activar(self, request, pk=None):
        """Activar producto"""
        product = self.get_object()
        product.is_active = True
        product.save()
        return Response({
            'message': 'Producto activado',
            'producto_id': product.id,
            'nombre': product.nombre
        })
