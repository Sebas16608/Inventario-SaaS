from rest_framework import serializers
from inventario.models import Category, Product, Stock, Movement


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'code', 'name', 'description', 'category', 'category_name',
            'sku', 'price', 'cost', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at']


class ProductDetailSerializer(ProductSerializer):
    """Serializer detallado de producto con stock"""
    stock = serializers.SerializerMethodField()
    
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['stock']
    
    def get_stock(self, obj):
        stocks = Stock.objects.filter(product=obj)
        return StockSerializer(stocks, many=True).data


class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    is_low_stock = serializers.BooleanField(read_only=True)
    is_overstock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Stock
        fields = [
            'id', 'product', 'product_name', 'warehouse', 'quantity',
            'minimum_quantity', 'maximum_quantity', 'is_low_stock',
            'is_overstock', 'last_updated'
        ]
        read_only_fields = ['last_updated']


class MovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    created_by_email = serializers.CharField(
        source='created_by.email',
        read_only=True
    )
    movement_type_display = serializers.CharField(
        source='get_movement_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = Movement
        fields = [
            'id', 'product', 'product_name', 'movement_type', 'movement_type_display',
            'quantity', 'warehouse', 'reference', 'notes', 'status', 'status_display',
            'created_by', 'created_by_email', 'moved_at'
        ]
        read_only_fields = ['moved_at', 'created_by']


class MovementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = [
            'product', 'movement_type', 'quantity', 'warehouse',
            'reference', 'notes'
        ]
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad debe ser mayor a 0"
            )
        return value


class MovementCompleteSerializer(serializers.Serializer):
    """Serializer para completar un movimiento"""
    def update(self, instance, validated_data):
        instance.complete()
        return instance
