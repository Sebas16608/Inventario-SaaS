from django.contrib import admin
from inventario.models import Category, Product, Stock, Movement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'is_active', 'created_at']
    list_filter = ['organization', 'is_active', 'created_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'sku', 'price', 'organization', 'is_active']
    list_filter = ['organization', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'sku']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'minimum_quantity', 'organization']
    list_filter = ['organization', 'warehouse', 'created_at']
    search_fields = ['product__name', 'warehouse']
    readonly_fields = ['last_updated']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(organization=request.user.organization)
        return queryset


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'status', 'created_by', 'moved_at']
    list_filter = ['organization', 'movement_type', 'status', 'moved_at']
    search_fields = ['product__name', 'reference']
    readonly_fields = ['moved_at', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('product', 'movement_type', 'quantity', 'warehouse')
        }),
        ('Detalles', {
            'fields': ('reference', 'notes', 'status')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'moved_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(organization=request.user.organization)
        return queryset

