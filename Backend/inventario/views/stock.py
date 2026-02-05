from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models

from inventario.models.stock import Stock
from inventario.serializers import StockSerializer
from utils.mixins import TenantFilterMixin


class StockViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar niveles de stock en almacenes.
    
    Endpoints disponibles:
    - GET /api/stock/ - Listar stock
    - POST /api/stock/ - Crear registro de stock
    - GET /api/stock/{id}/ - Detalles del stock
    - PUT /api/stock/{id}/ - Actualizar stock
    - PATCH /api/stock/{id}/ - Actualizar parcialmente
    - DELETE /api/stock/{id}/ - Eliminar registro de stock
    - GET /api/stock/alerts/ - Stock bajo alertas
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, TenantFilterMixin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization', 'product', 'warehouse']
    search_fields = ['product__name', 'warehouse']
    ordering_fields = ['quantity', 'updated_at']
    ordering = ['warehouse']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def alerts(self, request):
        """Obtener todos los productos con stock por debajo del mínimo"""
        queryset = self.get_queryset()
        low_stock = queryset.filter(quantity__lte=models.F('min_quantity'))
        
        serializer = StockSerializer(low_stock, many=True)
        return Response({
            'total_alerts': low_stock.count(),
            'stocks': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def summary(self, request):
        """Obtener resumen de stock por almacén"""
        queryset = self.get_queryset()
        warehouses = queryset.values('warehouse').distinct()
        
        summary = []
        for warehouse_data in warehouses:
            warehouse = warehouse_data['warehouse']
            warehouse_stocks = queryset.filter(warehouse=warehouse)
            total_items = warehouse_stocks.count()
            total_quantity = warehouse_stocks.aggregate(
                total=models.Sum('quantity')
            )['total'] or 0
            
            summary.append({
                'warehouse': warehouse,
                'total_products': total_items,
                'total_quantity': total_quantity
            })
        
        return Response(summary)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
