from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CategoryPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = CategoryPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        # Permitir leitura para todos, mas exigir autenticação para criar/editar/excluir
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
