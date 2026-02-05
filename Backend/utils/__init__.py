from django.db import models


class TenantModel(models.Model):
    """Modelo base para todas las entidades multi-tenant"""
    organization = models.ForeignKey(
        'accounts.Organization',
        on_delete=models.CASCADE,
        related_name='%(class)s_organization'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        """Asegurar que la organización está siempre establecida"""
        if not self.organization_id:
            raise ValueError("La organización es requerida")
        super().save(*args, **kwargs)
