from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class Product(models.Model):
    """Producto genérico del inventario adaptable por nicho.

    Contiene campos base compartidos y un `campos_extra` para datos
    específicos de farmacias o veterinarias.
    """
    empresa = models.ForeignKey(
        'accounts.Empresa',
        on_delete=models.PROTECT,
        related_name='products',
        null=True,
        blank=True,
        verbose_name='Empresa',
        help_text='Empresa propietaria del producto'
    )
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    categoria = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Categoría'
    )
    cantidad = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad',
        help_text='Cantidad disponible en inventario'
    )
    unidad_medida = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Unidad de medida',
        help_text='Ej: ml, unidades, caja'
    )
    stock_minimo = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock mínimo'
    )
    costo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Costo'
    )
    precio_venta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio de venta'
    )
    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Descuento',
        help_text='Porcentaje (ej: 10.00 = 10%)'
    )
    proveedor = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Proveedor/Distribuidor'
    )
    fecha_vencimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de vencimiento'
    )
    lote = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Lote'
    )
    campos_extra = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Campos extra',
        help_text='Ej farmacia: {"principio_activo":"paracetamol"}; veterinaria: {"especie":"gato"}'
    )
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')

    class Meta:
        unique_together = ('empresa', 'nombre')
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def clean(self):
        # Validación: la categoría debe pertenecer a la misma empresa
        if self.categoria and hasattr(self.categoria, 'empresa'):
            if self.categoria.empresa_id != self.empresa_id:
                raise ValidationError('La categoría debe pertenecer a la misma empresa')
        # Fecha de vencimiento no puede estar en el pasado al crear
        if self.fecha_vencimiento and self.fecha_vencimiento < timezone.now().date():
            raise ValidationError('La fecha de vencimiento no puede ser anterior a hoy')

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.cantidad < 0:
            raise ValidationError('La cantidad no puede ser negativa')
        super().save(*args, **kwargs)
