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
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<slug:slug>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/create/', TagCreateView.as_view(), name='tag_create'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag_detail'),
    path('tags/<slug:slug>/edit/', TagUpdateView.as_view(), name='tag_update'),
    path('tags/<slug:slug>/delete/', TagDeleteView.as_view(), name='tag_delete'),
]