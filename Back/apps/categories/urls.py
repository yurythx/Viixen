from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

# Criar router e registrar ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

# URLs da API
urlpatterns = [
    path('', include(router.urls)),
]
