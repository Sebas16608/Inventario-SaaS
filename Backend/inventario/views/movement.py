from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Count, Sum
from datetime import datetime, timedelta

from inventario.models.movement import Movement
from inventario.serializers import MovementSerializer, MovementCreateSerializer


class MovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar movimientos de inventario (ENTRADA/SALIDA).
    
    Endpoints disponibles:
    - GET /api/movements/ - Listar movimientos
    - POST /api/movements/ - Registrar movimiento
    - GET /api/movements/{id}/ - Detalles del movimiento
    - PUT /api/movements/{id}/ - Actualizar movimiento
    - PATCH /api/movements/{id}/ - Actualizar parcialmente
    - DELETE /api/movements/{id}/ - Eliminar movimiento
    - GET /api/movements/por-tipo/ - Movimientos por tipo (ENTRADA/SALIDA)
    - GET /api/movements/resumen/ - Resumen de movimientos
    - GET /api/movements/auditoria/ - Historial completo con filtros
    - POST /api/movements/{id}/revertir/ - Revertir un movimiento
    """
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['empresa', 'producto', 'tipo_movimiento']
    search_fields = ['producto__nombre', 'referencia', 'motivo', 'notas']
    ordering_fields = ['created_at', 'cantidad']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filtrar movimientos por empresa del usuario autenticado"""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if self.request.user.empresa:
                queryset = queryset.filter(empresa=self.request.user.empresa)
        return queryset
    
    def get_serializer_class(self):
        """Usar serializador específico para crear movimientos"""
        if self.action == 'create':
            return MovementCreateSerializer
        return MovementSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def por_tipo(self, request):
        """
        Obtener movimientos filtrados por tipo.
        Query params: tipo=ENTRADA|SALIDA
        """
        tipo_movimiento = request.query_params.get('tipo')
        queryset = self.get_queryset()
        
        if tipo_movimiento:
            queryset = queryset.filter(tipo_movimiento=tipo_movimiento)
        
        serializer = MovementSerializer(queryset, many=True)
        return Response({
            'tipo': tipo_movimiento or 'todos',
            'total': queryset.count(),
            'movimientos': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def resumen(self, request):
        """Resumen estadístico de movimientos por tipo"""
        queryset = self.get_queryset()
        
        # Estadísticas por tipo
        entradas = queryset.filter(tipo_movimiento='ENTRADA')
        salidas = queryset.filter(tipo_movimiento='SALIDA')
        
        resumen = {
            'entradas': {
                'total_movimientos': entradas.count(),
                'cantidad_total': entradas.aggregate(Sum('cantidad'))['cantidad__sum'] or 0,
                'valor_total': float(sum(
                    float(m.cantidad) * float(m.producto.costo)
                    for m in entradas if m.producto.costo
                ))
            },
            'salidas': {
                'total_movimientos': salidas.count(),
                'cantidad_total': salidas.aggregate(Sum('cantidad'))['cantidad__sum'] or 0,
                'valor_total': float(sum(
                    float(m.cantidad) * float(m.producto.precio_venta)
                    for m in salidas if m.producto.precio_venta
                ))
            },
            'total_movimientos': queryset.count(),
            'periodo_ultimos_7_dias': queryset.filter(
                created_at__gte=datetime.now() - timedelta(days=7)
            ).count()
        }
        
        return Response(resumen)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def auditoria(self, request):
        """Historial completo de movimientos con filtros avanzados"""
        queryset = self.get_queryset()
        
        # Aplicar filtros opcionales
        producto_id = request.query_params.get('producto_id')
        tipo = request.query_params.get('tipo')
        usuario_id = request.query_params.get('usuario_id')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        if tipo:
            queryset = queryset.filter(tipo_movimiento=tipo)
        if usuario_id:
            queryset = queryset.filter(creado_por_id=usuario_id)
        if fecha_inicio:
            queryset = queryset.filter(created_at__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(created_at__lte=fecha_fin)
        
        serializer = MovementSerializer(queryset, many=True)
        return Response({
            'total': queryset.count(),
            'filtros_aplicados': {
                'producto_id': producto_id,
                'tipo': tipo,
                'usuario_id': usuario_id,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            },
            'movimientos': serializer.data
        })
    
    def perform_create(self, serializer):
        """Crear movimiento y asignar usuario que lo creó"""
        if self.request.user.empresa:
            serializer.save(
                empresa=self.request.user.empresa,
                creado_por=self.request.user
            )
        else:
            serializer.save(creado_por=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def revertir(self, request, pk=None):
        """Revertir un movimiento creando uno de tipo opuesto"""
        movimiento = self.get_object()
        
        # Determinar tipo opuesto
        tipo_opuesto = 'SALIDA' if movimiento.tipo_movimiento == 'ENTRADA' else 'ENTRADA'
        
        # Crear movimiento de reversión
        movimiento_reversado = Movement.objects.create(
            empresa=movimiento.empresa,
            producto=movimiento.producto,
            tipo_movimiento=tipo_opuesto,
            cantidad=movimiento.cantidad,
            referencia=f"REVERSA-{movimiento.id}",
            motivo='Reversión de movimiento',
            notas=f'Reversión del movimiento {movimiento.id} creado el {movimiento.created_at}',
            creado_por=request.user
        )
        
        return Response({
            'message': 'Movimiento revertido exitosamente',
            'movimiento_original_id': movimiento.id,
            'movimiento_reversado_id': movimiento_reversado.id,
            'tipo_reversado': tipo_opuesto,
            'cantidad': movimiento.cantidad,
            'producto': movimiento.producto.nombre
        }, status=status.HTTP_201_CREATED)
