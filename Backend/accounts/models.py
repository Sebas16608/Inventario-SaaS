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
    """Modelo de Empresa (Tenant multi-nicho)"""
    nombre = models.CharField(max_length=255, unique=True, verbose_name='Nombre')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    logo = models.ImageField(upload_to='empresas/', null=True, blank=True, verbose_name='Logo')
    nicho = models.CharField(
        max_length=50,
        choices=[('farmacia', 'Farmacia'), ('veterinaria', 'Veterinaria')],
        verbose_name='Nicho',
        help_text='Sector de negocio de la empresa'
    )
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
    
    def __str__(self):
        return self.nombre


class Role(models.Model):
    """Roles disponibles en la empresa"""
    ROLE_CHOICES = [
        ('admin', _('Administrador')),
        ('manager', _('Gerente')),
        ('staff', _('Personal')),
        ('viewer', _('Visualizador')),
    ]
    
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='roles',
        null=True,
        blank=True,
        verbose_name='Empresa'
    )
    nombre = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    permissions = models.ManyToManyField(
        'Permission',
        blank=True,
        related_name='roles',
        verbose_name='Permisos'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    
    class Meta:
        unique_together = ('empresa', 'nombre')
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return f"{self.get_nombre_display()} - {self.empresa.nombre if self.empresa else 'Sin empresa'}"


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
    """Usuario personalizado con relación a Empresa"""
    email = models.EmailField(unique=True, verbose_name='Email')
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='usuarios',
        null=True,
        blank=True,
        verbose_name='Empresa'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        verbose_name='Rol'
    )
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
    
    def has_permission(self, permission_code):
        """Verifica si el usuario tiene un permiso específico"""
        if self.is_superuser:
            return True
        if self.role is None:
            return False
        return self.role.permissions.filter(code=permission_code).exists()
