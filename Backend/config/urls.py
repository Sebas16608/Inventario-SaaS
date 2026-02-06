"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Import ViewSets
from accounts.views import (
    UserViewSet,
    EmpresaViewSet,
)
from inventario.views import (
    CategoryViewSet,
    ProductViewSet,
    MovementViewSet,
)

# Configure router
router = DefaultRouter()

# Accounts routes
router.register(r'users', UserViewSet, basename='user')
router.register(r'empresas', EmpresaViewSet, basename='empresa')

# Inventario routes
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'movements', MovementViewSet, basename='movement')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Endpoints
    path('api/', include(router.urls)),
    
    # Swagger/OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
