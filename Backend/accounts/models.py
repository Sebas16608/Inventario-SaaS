from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Manager personalizado para el modelo User"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El email es requerido'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Empresa(models.Model):
    """Modelo de Empresa (Tenant multi-nicho) - MVP Simplificado"""
    
    nombre = models.CharField(max_length=255, unique=True, verbose_name='Nombre')
    nicho = models.CharField(
        max_length=50,
        choices=[('farmacia', 'Farmacia'), ('veterinaria', 'Veterinaria')],
        verbose_name='Nicho',
        help_text='Sector de negocio de la empresa'
    )
    direccion = models.CharField(max_length=255, blank=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
    
    def __str__(self):
        return self.nombre


class User(AbstractUser):
    """Usuario personalizado - MVP Simplificado"""
    
    email = models.EmailField(unique=True, verbose_name='Email')
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='usuarios',
        null=True,
        blank=True,
        verbose_name='Empresa'
    )
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
