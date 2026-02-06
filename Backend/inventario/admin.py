from django.contrib import admin
from inventario.models import Category, Product, Movement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'is_active', 'created_at']
    list_filter = ['empresa', 'is_active', 'created_at']
    search_fields = ['nombre']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información', {'fields': ('empresa', 'nombre', 'descripcion')}),
        ('Campos Extra', {'fields': ('campos_extra',), 'classes': ('collapse',)}),
        ('Estado', {'fields': ('is_active',)}),
        ('Fechas', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'empresa', 'cantidad', 'precio_venta', 'is_active']
    list_filter = ['empresa', 'categoria', 'is_active', 'created_at']
    search_fields = ['nombre', 'proveedor']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {'fields': ('empresa', 'nombre', 'categoria')}),
        ('Inventario', {
            'fields': ('cantidad', 'unidad_medida', 'stock_minimo'),
            'description': 'Gestión de stock y unidades'
        }),
        ('Precios y Costos', {
            'fields': ('costo', 'precio_venta', 'descuento'),
        }),
        ('Detalles de Producto', {
            'fields': ('proveedor', 'fecha_vencimiento', 'lote'),
        }),
        ('Campos Específicos por Nicho', {
            'fields': ('campos_extra',),
            'classes': ('collapse',),
            'description': 'Información adicional según el nicho (farmacia/veterinaria)'
        }),
        ('Estado', {'fields': ('is_active',)}),
        ('Auditoría', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'empresa', 'created_by', 'created_at']
    list_filter = ['empresa', 'movement_type', 'created_at']
    search_fields = ['product__nombre', 'referencia', 'motivo']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('empresa', 'product', 'movement_type', 'quantity')
        }),
        ('Detalles', {
            'fields': ('referencia', 'motivo', 'notes')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(empresa=request.user.empresa)
        return queryset

