"""
Tests para los modelos, serializers y views de inventario.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from inventario.models.category import Category
from inventario.models.product import Product
from inventario.models.movement import Movement
from accounts.models import Empresa, Role, Permission


User = get_user_model()


class EmpresaModelTest(TestCase):
    """Tests para el modelo Empresa"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nombre='Farmacia Test',
            slug='farmacia-test',
            descripcion='Empresa de prueba',
            nicho='farmacia'
        )
    
    def test_empresa_creation(self):
        """Test que verifica la creación de una Empresa"""
        self.assertEqual(self.empresa.nombre, 'Farmacia Test')
        self.assertEqual(self.empresa.nicho, 'farmacia')
        self.assertTrue(self.empresa.is_active)
    
    def test_empresa_str(self):
        """Test que verifica el string representation"""
        self.assertEqual(str(self.empresa), 'Farmacia Test')


class CategoryModelTest(TestCase):
    """Tests para el modelo Category"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nombre='Farmacia Test',
            slug='farmacia-test',
            nicho='farmacia'
        )
        self.categoria = Category.objects.create(
            empresa=self.empresa,
            nombre='Medicamentos',
            descripcion='Medicamentos en general',
            campos_extra={'tipo_regulacion': 'controlado'}
        )
    
    def test_category_creation(self):
        """Test que verifica la creación de una Categoría"""
        self.assertEqual(self.categoria.nombre, 'Medicamentos')
        self.assertEqual(self.categoria.empresa, self.empresa)
        self.assertIn('tipo_regulacion', self.categoria.campos_extra)
    
    def test_category_str(self):
        """Test que verifica el string representation"""
        self.assertEqual(str(self.categoria), 'Medicamentos')


class ProductModelTest(TestCase):
    """Tests para el modelo Product"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nombre='Farmacia Test',
            slug='farmacia-test',
            nicho='farmacia'
        )
        self.categoria = Category.objects.create(
            empresa=self.empresa,
            nombre='Medicamentos'
        )
        self.producto = Product.objects.create(
            empresa=self.empresa,
            nombre='Paracetamol 500mg',
            categoria=self.categoria,
            cantidad=100,
            stock_minimo=10,
            costo=5.00,
            precio_venta=10.00,
            unidad_medida='tableta',
            campos_extra={'principio_activo': 'paracetamol'}
        )
    
    def test_product_creation(self):
        """Test que verifica la creación de un Producto"""
        self.assertEqual(self.producto.nombre, 'Paracetamol 500mg')
        self.assertEqual(self.producto.cantidad, 100)
        self.assertEqual(self.producto.costo, 5.00)
    
    def test_product_str(self):
        """Test que verifica el string representation"""
        self.assertEqual(str(self.producto), 'Paracetamol 500mg')
    
    def test_product_campos_extra(self):
        """Test que verifica los campos extra en JSONField"""
        self.assertIn('principio_activo', self.producto.campos_extra)
        self.assertEqual(self.producto.campos_extra['principio_activo'], 'paracetamol')


class MovementModelTest(TestCase):
    """Tests para el modelo Movement"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nombre='Farmacia Test',
            slug='farmacia-test',
            nicho='farmacia'
        )
        self.usuario = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123',
            empresa=self.empresa
        )
        self.categoria = Category.objects.create(
            empresa=self.empresa,
            nombre='Medicamentos'
        )
        self.producto = Product.objects.create(
            empresa=self.empresa,
            nombre='Paracetamol 500mg',
            categoria=self.categoria,
            cantidad=100,
            stock_minimo=10,
            costo=5.00,
            precio_venta=10.00
        )
    
    def test_movement_entrada_creation(self):
        """Test que verifica la creación de un movimiento de ENTRADA"""
        movimiento = Movement.objects.create(
            empresa=self.empresa,
            producto=self.producto,
            tipo_movimiento='ENTRADA',
            cantidad=50,
            referencia='FACT-001',
            creado_por=self.usuario
        )
        self.assertEqual(movimiento.tipo_movimiento, 'ENTRADA')
        self.assertEqual(movimiento.cantidad, 50)
    
    def test_movement_auto_update_stock(self):
        """Test que verifica la actualización automática de stock"""
        # Stock inicial: 100
        inicial = self.producto.cantidad
        
        # Crear movimiento de entrada
        Movement.objects.create(
            empresa=self.empresa,
            producto=self.producto,
            tipo_movimiento='ENTRADA',
            cantidad=50,
            creado_por=self.usuario
        )
        
        # Refrescar el producto
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, inicial + 50)
