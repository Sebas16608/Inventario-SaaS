from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone


class Movement(models.Model):
    """Movimiento de inventario (ENTRADA / SALIDA).

    Al guardarse, actualiza automáticamente `Product.cantidad`.
    """
    TIPO_ENTRADA = 'ENTRADA'
    TIPO_SALIDA = 'SALIDA'
    MOVEMENT_TYPES = [
        (TIPO_ENTRADA, 'Entrada'),
        (TIPO_SALIDA, 'Salida'),
    ]

    empresa = models.ForeignKey(
        'accounts.Empresa',
        on_delete=models.PROTECT,
        related_name='movements',
        null=True,
        blank=True,
        verbose_name='Empresa',
        help_text='Empresa responsable del movimiento'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name='Producto'
    )
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES,
        verbose_name='Tipo de movimiento'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad'
    )
    referencia = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Referencia',
        help_text='Número de factura, orden de compra u otra referencia'
    )
    motivo = models.TextField(blank=True, verbose_name='Motivo')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='movements_created',
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.nombre} ({self.quantity})"

    def clean(self):
        # Validaciones básicas
        if self.product and self.empresa and hasattr(self.product, 'empresa'):
            if self.product.empresa_id != self.empresa_id:
                raise ValidationError('El producto debe pertenecer a la misma empresa')

    def save(self, *args, **kwargs):
        """Al guardar, aplicar cambio de stock en `Product.cantidad`.

        - En creación: aplica directamente.
        - En actualización: revierte el efecto anterior y aplica el nuevo.
        Se asegura con `transaction.atomic` y `select_for_update` para evitar
        condiciones de carrera.
        """
        self.full_clean()

        with transaction.atomic():
            product = self.product.__class__.objects.select_for_update().get(pk=self.product.pk)

            if not self.pk:
                # Creación
                if self.movement_type == self.TIPO_SALIDA and self.quantity > product.cantidad:
                    raise ValidationError('Stock insuficiente para realizar la salida')

                if self.movement_type == self.TIPO_ENTRADA:
                    product.cantidad = product.cantidad + self.quantity
                else:
                    product.cantidad = product.cantidad - self.quantity

                if product.cantidad < 0:
                    raise ValidationError('Resultado de stock inválido (negativo)')

                product.save()
                super().save(*args, **kwargs)
                return

            # Actualización de movimiento existente: revertir efecto previo y aplicar nuevo
            prev = Movement.objects.select_for_update().get(pk=self.pk)

            # Revertir efecto del previo
            if prev.movement_type == self.TIPO_ENTRADA:
                product.cantidad = product.cantidad - prev.quantity
            else:
                product.cantidad = product.cantidad + prev.quantity

            # Aplicar nuevo efecto
            if self.movement_type == self.TIPO_SALIDA and self.quantity > product.cantidad:
                raise ValidationError('Stock insuficiente para la actualización del movimiento')

            if self.movement_type == self.TIPO_ENTRADA:
                product.cantidad = product.cantidad + self.quantity
            else:
                product.cantidad = product.cantidad - self.quantity

            if product.cantidad < 0:
                raise ValidationError('Resultado de stock inválido (negativo)')

            product.save()
            super().save(*args, **kwargs)
