from django.db import models


class Category(models.Model):
    """Categoría de productos.

    Modelo genérico adaptable a distintos nichos (farmacias, veterinarias).
    Se relaciona con `accounts.Empresa` mediante la FK `empresa`.
    """
    empresa = models.ForeignKey(
        'accounts.Empresa',
        on_delete=models.PROTECT,
        related_name='categories',
        null=True,
        blank=True,
        verbose_name='Empresa',
        help_text='Empresa propietaria de la categoría'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre de la categoría'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción opcional de la categoría'
    )
    campos_extra = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Campos extra',
        help_text='Datos específicos por nicho. Ej: {"tipo_medicamento": "controlado"} o {"especie": "perro"}'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si la categoría está activa'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')

    class Meta:
        unique_together = ('empresa', 'nombre')
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
