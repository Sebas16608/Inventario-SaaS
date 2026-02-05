from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models

from inventario.models.product import Product
from inventario.serializers import ProductSerializer, StockSerializer
from utils.mixins import TenantFilterMixin


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
    - GET /api/products/{id}/stock/ - Stock disponible
    - POST /api/products/{id}/low_stock/ - Productos con stock bajo
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, TenantFilterMixin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization', 'category', 'is_active']
    search_fields = ['name', 'code', 'sku', 'description']
    ordering_fields = ['name', 'price', 'created_at']
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
    def stock(self, request, pk=None):
        """Obtener información de stock del producto"""
        product = self.get_object()
        stocks = product.stocks.all()
        
        serializer = StockSerializer(stocks, many=True)
        return Response({
            'product_id': product.id,
            'product_name': product.name,
            'stocks': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def low_stock(self, request):
        """Obtener productos con stock bajo"""
        queryset = self.get_queryset()
        products = queryset.filter(
            stocks__quantity__lte=models.F('stocks__min_quantity')
        ).distinct()
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def deactivate(self, request, pk=None):
        """Desactivar producto"""
        product = self.get_object()
        product.is_active = False
        product.save()
        return Response({'message': 'Producto desactivado'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def activate(self, request, pk=None):
        """Activar producto"""
        product = self.get_object()
        product.is_active = True
        product.save()
        return Response({'message': 'Producto activado'})
