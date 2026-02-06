from rest_framework import serializers
from inventario.models import Category, Product, Movement


class CategorySerializer(serializers.ModelSerializer):
    """Serializador de categorías con campos específicos del nicho"""
    
    class Meta:
        model = Category
        fields = [
            'id', 'empresa', 'nombre', 'descripcion', 'campos_extra',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serializador básico de productos"""
    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )
    empresa_nombre = serializers.CharField(
        source='empresa.nombre',
        read_only=True
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'empresa', 'empresa_nombre', 'categoria', 'categoria_nombre',
            'nombre', 'cantidad', 'unidad_medida', 'stock_minimo',
            'costo', 'precio_venta', 'descuento', 'proveedor',
            'fecha_vencimiento', 'lote', 'campos_extra',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductDetailSerializer(ProductSerializer):
    """Serializador detallado de productos con información adicional"""
    stock_disponible = serializers.IntegerField(source='cantidad', read_only=True)
    precio_total = serializers.SerializerMethodField()
    margen_ganancia = serializers.SerializerMethodField()
    
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + [
            'stock_disponible', 'precio_total', 'margen_ganancia'
        ]
    
    def get_precio_total(self, obj):
        """Calcula el precio total considerando descuento"""
        if obj.precio_venta and obj.descuento:
            return obj.precio_venta * (1 - obj.descuento / 100)
        return obj.precio_venta
    
    def get_margen_ganancia(self, obj):
        """Calcula el margen de ganancia porcentual"""
        if obj.costo and obj.precio_venta:
            precio_final = self.get_precio_total(obj)
            return ((precio_final - obj.costo) / obj.costo * 100) if obj.costo > 0 else 0
        return 0


class MovementSerializer(serializers.ModelSerializer):
    """Serializador de movimientos de inventario"""
    producto_nombre = serializers.CharField(
        source='producto.nombre',
        read_only=True
    )
    empresa_nombre = serializers.CharField(
        source='empresa.nombre',
        read_only=True
    )
    creado_por_email = serializers.CharField(
        source='creado_por.email',
        read_only=True
    )
    tipo_movimiento_display = serializers.CharField(
        source='get_tipo_movimiento_display',
        read_only=True
    )
    
    class Meta:
        model = Movement
        fields = [
            'id', 'empresa', 'empresa_nombre', 'producto', 'producto_nombre',
            'tipo_movimiento', 'tipo_movimiento_display', 'cantidad',
            'referencia', 'motivo', 'notas', 'creado_por', 'creado_por_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'creado_por']


class MovementCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear movimientos de inventario"""
    
    class Meta:
        model = Movement
        fields = [
            'producto', 'tipo_movimiento', 'cantidad', 'referencia',
            'motivo', 'notas'
        ]
    
    def validate_cantidad(self, value):
        """Valida que la cantidad sea positiva"""
        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad debe ser mayor a 0"
            )
        return value
    
    def validate(self, data):
        """Valida la salida de inventario"""
        producto = data.get('producto')
        tipo_movimiento = data.get('tipo_movimiento')
        cantidad = data.get('cantidad')
        
        if tipo_movimiento == 'SALIDA' and producto:
            if producto.cantidad < cantidad:
                raise serializers.ValidationError({
                    'cantidad': f"Stock insuficiente. Disponible: {producto.cantidad}"
                })
        
        return data


__all__ = ['CategorySerializer', 'ProductSerializer', 'ProductDetailSerializer', 
           'MovementSerializer', 'MovementCreateSerializer']
