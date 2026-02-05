from django.db import models
from django.core.validators import MinValueValidator
from utils import TenantModel


class Product(TenantModel):
    """Producto del inventario"""
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='products'
    )
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('organization', 'code')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Asegurar que la categoría pertenece a la misma organización
        if self.category.organization != self.organization:
            raise ValueError("La categoría debe pertenecer a la misma organización")
        super().save(*args, **kwargs)
