from django.urls import path
from .views.post.list import PostListView
from .views.post.detail import PostDetailView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]