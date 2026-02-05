from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from inventario.models.movement import Movement
from inventario.serializers import MovementSerializer
from utils.mixins import TenantFilterMixin


class MovementViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar movimientos de inventario.
    
    Endpoints disponibles:
    - GET /api/movements/ - Listar movimientos
    - POST /api/movements/ - Registrar movimiento
    - GET /api/movements/{id}/ - Detalles del movimiento
    - PUT /api/movements/{id}/ - Actualizar movimiento
    - PATCH /api/movements/{id}/ - Actualizar parcialmente
    - DELETE /api/movements/{id}/ - Eliminar movimiento
    - GET /api/movements/by_type/?type=IN - Movimientos por tipo
    - GET /api/movements/audit/ - Historial de auditoría
    """
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    permission_classes = [IsAuthenticated, TenantFilterMixin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization', 'product', 'movement_type', 'warehouse']
    search_fields = ['product__name', 'warehouse', 'reason', 'notes']
    ordering_fields = ['created_at', 'quantity']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            queryset = queryset.filter(organization=self.request.user.organization)
        return queryset
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_type(self, request):
        """
        Obtener movimientos filtrados por tipo.
        Query params: type=IN|OUT|ADJUSTMENT|TRANSFER
        """
        movement_type = request.query_params.get('type')
        queryset = self.get_queryset()
        
        if movement_type:
            queryset = queryset.filter(movement_type=movement_type)
        
        serializer = MovementSerializer(queryset, many=True)
        return Response({
            'type': movement_type or 'all',
            'total_count': queryset.count(),
            'movements': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def audit(self, request):
        """Historial de auditoría - todos los movimientos con detalles"""
        queryset = self.get_queryset()
        
        # Aplicar filtros si existen
        product_id = request.query_params.get('product_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        serializer = MovementSerializer(queryset, many=True)
        return Response({
            'total_movements': queryset.count(),
            'movements': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def summary(self, request):
        """Resumen de movimientos por tipo"""
        queryset = self.get_queryset()
        
        summary = {
            'IN': queryset.filter(movement_type='IN').count(),
            'OUT': queryset.filter(movement_type='OUT').count(),
            'ADJUSTMENT': queryset.filter(movement_type='ADJUSTMENT').count(),
            'TRANSFER': queryset.filter(movement_type='TRANSFER').count(),
            'total': queryset.count()
        }
        
        return Response(summary)
    
    def perform_create(self, serializer):
        movement = serializer.save(created_by=self.request.user)
        # El modelo automáticamente actualiza el stock al guardarse
        return movement
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reverse(self, request, pk=None):
        """Revertir un movimiento (crear uno contrario)"""
        movement = self.get_object()
        
        # Crear movimiento opuesto
        reverse_type = {
            'IN': 'OUT',
            'OUT': 'IN',
            'ADJUSTMENT': 'ADJUSTMENT',
            'TRANSFER': 'TRANSFER'
        }
        
        Movement.objects.create(
            organization=movement.organization,
            product=movement.product,
            movement_type=reverse_type[movement.movement_type],
            warehouse=movement.warehouse,
            quantity=movement.quantity,
            reason='REVERSE',
            notes=f'Reversión del movimiento {movement.id}',
            created_by=request.user
        )
        
        return Response({
            'message': 'Movimiento revertido correctamente',
            'original_movement': movement.id
        })
