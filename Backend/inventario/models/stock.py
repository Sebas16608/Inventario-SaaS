from django.db import models
from django.core.validators import MinValueValidator
from utils import TenantModel


class Stock(TenantModel):
    """Stock de productos por almacén"""
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='stock'
    )
    warehouse = models.CharField(
        max_length=100,
        default='Principal',
        help_text='Nombre del almacén o ubicación'
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    minimum_quantity = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        help_text='Cantidad mínima para alertas'
    )
    maximum_quantity = models.IntegerField(
        default=1000,
        validators=[MinValueValidator(0)],
        help_text='Cantidad máxima del almacén'
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('organization', 'product', 'warehouse')
        verbose_name_plural = 'Stocks'
        ordering = ['warehouse', 'product']
    
    def __str__(self):
        return f"{self.product.name} - {self.warehouse} ({self.quantity})"
    
    @property
    def is_low_stock(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.quantity < self.minimum_quantity
    
    @property
    def is_overstock(self):
        """Verifica si el stock está por encima del máximo"""
        return self.quantity > self.maximum_quantity
    
    def save(self, *args, **kwargs):
        # Asegurar que el producto pertenece a la misma organización
        if self.product.organization != self.organization:
            raise ValueError("El producto debe pertenecer a la misma organización")
        super().save(*args, **kwargs)
