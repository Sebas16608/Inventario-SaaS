from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customiza el serializador de JWT para aceptar email en lugar de username.
    """
    username_field = User.USERNAME_FIELD
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover el campo username y agregar email
        self.fields.pop(self.username_field, None)
        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Valida las credenciales usando email y contraseña.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Buscar usuario por email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = 'No se encontró usuario con ese email.'
                raise serializers.ValidationError(msg, code='authentication')

            # Verificar contraseña
            if not user.check_password(password):
                msg = 'Contraseña incorrecta.'
                raise serializers.ValidationError(msg, code='authentication')

            # Verificar que el usuario esté activo
            if not user.is_active:
                msg = 'Este usuario está desactivado.'
                raise serializers.ValidationError(msg, code='authentication')
        else:
            msg = 'Se requieren email y contraseña.'
            raise serializers.ValidationError(msg, code='authentication')

        # Obtener los tokens
        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista customizada para obtener tokens usando email en lugar de username.
    """
    serializer_class = CustomTokenObtainPairSerializer
