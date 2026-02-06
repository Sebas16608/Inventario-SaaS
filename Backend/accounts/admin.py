from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nicho', 'email', 'telefono', 'is_active', 'created_at']
    list_filter = ['is_active', 'nicho', 'created_at']
    search_fields = ['nombre', 'email', 'telefono']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {'fields': ('nombre', 'nicho')}),
        ('Contacto', {'fields': ('email', 'telefono', 'direccion')}),
        ('Estado', {'fields': ('is_active',)}),
        ('Fechas', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'empresa', 'is_active']
    list_filter = ['is_active', 'empresa', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'telefono')}),
        ('Empresa', {'fields': ('empresa',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'empresa'),
        }),
    )
    
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'last_login']

