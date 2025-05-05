from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CommentPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    pagination_class = ArticlePagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        # Permitir leitura para todos, mas exigir autenticação para criar/editar/excluir
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        # Permitir leitura para todos, mas exigir autenticação para criar/editar/excluir
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        """Filtrar comentários por artigo se o parâmetro 'article_slug' estiver presente"""
        queryset = Comment.objects.all()
        article_slug = self.request.query_params.get('article_slug', None)
        if article_slug:
            article = get_object_or_404(Article, slug=article_slug)
            queryset = queryset.filter(article=article)
        return queryset