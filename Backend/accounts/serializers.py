from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Empresa

User = get_user_model()


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para Empresa - MVP Simplificado"""
    
    class Meta:
        model = Empresa
        fields = [
            'id', 'nombre', 'nicho', 'direccion', 'telefono', 
            'email', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para User"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'telefono',
            'empresa', 'empresa_nombre', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Crear usuario con contraseña hasheada"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(UserSerializer):
    """Serializer detallado de User con más información"""
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'is_staff', 'is_superuser', 'username', 'last_login'
        ]
        read_only_fields = UserSerializer.Meta.read_only_fields + [
            'is_staff', 'is_superuser', 'last_login'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear nuevos usuarios"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 
            'last_name', 'telefono', 'empresa', 'username'
        ]
    
    def validate(self, data):
        """Validar que las contraseñas coincidan"""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden'})
        return data
    
    def create(self, validated_data):
        """Crear usuario con contraseña"""
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Las contraseñas no coinciden'}
            )
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'is_active']
