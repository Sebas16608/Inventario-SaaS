from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models

from inventario.models.category import Category
from inventario.serializers import CategorySerializer, ProductSerializer


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
    - GET /api/categories/{id}/productos/ - Productos de la categoría
    - POST /api/categories/{id}/desactivar/ - Desactivar categoría
    - POST /api/categories/{id}/activar/ - Activar categoría
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['empresa', 'is_active']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']
    
    def get_queryset(self):
        """Filtrar categorías por empresa del usuario autenticado"""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if self.request.user.empresa:
                queryset = queryset.filter(empresa=self.request.user.empresa)
        return queryset
    
    def perform_create(self, serializer):
        """Asignar la empresa del usuario al crear categoría"""
        if self.request.user.empresa:
            serializer.save(empresa=self.request.user.empresa)
        else:
            serializer.save()
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def productos(self, request, pk=None):
        """Obtener todos los productos de esta categoría"""
        categoria = self.get_object()
        productos = categoria.products.all()
        
        serializer = ProductSerializer(productos, many=True)
        
        return Response({
            'categoria_id': categoria.id,
            'categoria_nombre': categoria.nombre,
            'total_productos': productos.count(),
            'productos': serializer.data
        })
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def resumen(self, request, pk=None):
        """Obtener resumen de la categoría (cantidad de productos, stock total, etc.)"""
        categoria = self.get_object()
        productos = categoria.products.all()
        
        stock_total = sum(p.cantidad for p in productos)
        valor_inventario = sum(
            float(p.cantidad) * float(p.costo) 
            for p in productos if p.costo
        )
        productos_bajo_stock = productos.filter(
            cantidad__lt=models.F('stock_minimo')
        ).count()
        
        return Response({
            'categoria_id': categoria.id,
            'categoria_nombre': categoria.nombre,
            'total_productos': productos.count(),
            'stock_total': stock_total,
            'valor_inventario': float(valor_inventario),
            'productos_bajo_stock': productos_bajo_stock,
            'campos_extra': categoria.campos_extra,
            'is_active': categoria.is_active
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def desactivar(self, request, pk=None):
        """Desactivar categoría"""
        categoria = self.get_object()
        categoria.is_active = False
        categoria.save()
        return Response({
            'message': 'Categoría desactivada',
            'categoria_id': categoria.id,
            'nombre': categoria.nombre
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def activar(self, request, pk=None):
        """Activar categoría"""
        categoria = self.get_object()
        categoria.is_active = True
        categoria.save()
        return Response({
            'message': 'Categoría activada',
            'categoria_id': categoria.id,
            'nombre': categoria.nombre
        })
