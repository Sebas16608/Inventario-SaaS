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


class Organization(models.Model):
    """Modelo de Organización (Tenant)"""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='organizations/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Organización')
        verbose_name_plural = _('Organizaciones')
    
    def __str__(self):
        return self.name


class Role(models.Model):
    """Roles disponibles en la organización"""
    ROLE_CHOICES = [
        ('admin', _('Administrador')),
        ('manager', _('Gerente')),
        ('staff', _('Personal')),
        ('viewer', _('Visualizador')),
    ]
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    name = models.CharField(max_length=50, choices=ROLE_CHOICES)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        'Permission',
        blank=True,
        related_name='roles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('organization', 'name')
        verbose_name = _('Rol')
        verbose_name_plural = _('Roles')
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.organization.name}"


class Permission(models.Model):
    """Permisos granulares del sistema"""
    PERMISSION_CHOICES = [
        ('create_product', _('Crear productos')),
        ('edit_product', _('Editar productos')),
        ('delete_product', _('Eliminar productos')),
        ('view_product', _('Ver productos')),
        ('create_movement', _('Crear movimientos')),
        ('edit_movement', _('Editar movimientos')),
        ('delete_movement', _('Eliminar movimientos')),
        ('view_movement', _('Ver movimientos')),
        ('view_reports', _('Ver reportes')),
        ('manage_users', _('Gestionar usuarios')),
    ]
    
    code = models.CharField(max_length=50, unique=True, choices=PERMISSION_CHOICES)
    description = models.TextField()
    
    class Meta:
        verbose_name = _('Permiso')
        verbose_name_plural = _('Permisos')
    
    def __str__(self):
        return self.get_code_display()


class CustomUser(AbstractUser):
    """User personalizado con relación a Organization"""
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def has_permission(self, permission_code):
        """Verifica si el usuario tiene un permiso específico"""
        if self.is_superuser:
            return True
        if self.role is None:
            return False
        return self.role.permissions.filter(code=permission_code).exists()
