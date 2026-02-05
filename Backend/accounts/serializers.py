from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organization, Role, Permission

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'description']


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'description', 'logo', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class CustomUserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'organization', 
            'role', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at']


class CustomUserDetailSerializer(CustomUserSerializer):
    """Serializer detallado para un usuario"""
    permissions = serializers.SerializerMethodField()
    
    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ['permissions']
    
    def get_permissions(self, obj):
        """Obtiene los permisos del usuario"""
        if obj.role:
            return PermissionSerializer(
                obj.role.permissions.all(),
                many=True
            ).data
        return []


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']
    
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


class RoleCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True
    )
    
    class Meta:
        model = Role
        fields = ['name', 'description', 'permissions']
