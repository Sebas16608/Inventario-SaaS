from django.db import models
from django.core.validators import MinValueValidator
from utils import TenantModel
from .stock import Stock


class Movement(TenantModel):
    """Movimiento de inventario (entrada/salida)"""
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Salida'),
        ('adjustment', 'Ajuste'),
        ('transfer', 'Transferencia'),
    ]
    
    MOVEMENT_STATUS = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]
    
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='movements'
    )
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    warehouse = models.CharField(max_length=100, default='Principal')
    reference = models.CharField(
        max_length=100,
        blank=True,
        help_text='Número de referencia (factura, OC, etc)'
    )
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=MOVEMENT_STATUS,
        default='pending'
    )
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='movements_created'
    )
    moved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-moved_at']
        verbose_name_plural = 'Movements'
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        # Asegurar que el producto pertenece a la misma organización
        if self.product.organization != self.organization:
            raise ValueError("El producto debe pertenecer a la misma organización")
        super().save(*args, **kwargs)
    
    def complete(self):
        """Completa el movimiento y actualiza el stock"""
        if self.status != 'pending':
            raise ValueError("Solo se pueden completar movimientos pendientes")
        
        stock, created = Stock.objects.get_or_create(
            organization=self.organization,
            product=self.product,
            warehouse=self.warehouse,
            defaults={'quantity': 0}
        )
        
        if self.movement_type == 'in':
            stock.quantity += self.quantity
        elif self.movement_type == 'out':
            if stock.quantity < self.quantity:
                raise ValueError("Stock insuficiente")
            stock.quantity -= self.quantity
        elif self.movement_type == 'adjustment':
            stock.quantity = self.quantity
        
        stock.save()
        self.status = 'completed'
        self.save(update_fields=['status'])
