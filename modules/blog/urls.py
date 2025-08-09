from django.urls import path
from .views.post.list import PostListView
from .views.post.detail import PostDetailView
from .views.post.crud import PostCreateView, PostUpdateView, PostDeleteView
from .views.category import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from .views.tag import TagListView, TagDetailView, TagCreateView, TagUpdateView, TagDeleteView

app_name = 'blog'

urlpatterns = [
    # Posts
    path('', PostListView.as_view(), name='post_list'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/create/', TagCreateView.as_view(), name='tag_create'),
    path('tag/<slug:slug>/', TagDetailView.as_view(), name='tag_detail'),
    path('tag/<int:pk>/edit/', TagUpdateView.as_view(), name='tag_update'),
    path('tag/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),
]