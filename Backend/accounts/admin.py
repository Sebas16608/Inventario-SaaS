from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Empresa, Role, Permission


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'nicho', 'is_active', 'created_at']
    list_filter = ['is_active', 'nicho', 'created_at']
    search_fields = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {'fields': ('nombre', 'slug', 'nicho')}),
        ('Descripción', {'fields': ('descripcion', 'logo')}),
        ('Estado', {'fields': ('is_active',)}),
        ('Fechas', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['code', 'description']
    search_fields = ['code', 'description']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'created_at']
    list_filter = ['empresa', 'nombre']
    search_fields = ['nombre', 'empresa__nombre']
    filter_horizontal = ['permissions']
    readonly_fields = ['created_at']


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'empresa', 'role', 'is_active']
    list_filter = ['is_active', 'empresa', 'role', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name')}),
        ('Empresa', {'fields': ('empresa', 'role')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'last_login']

