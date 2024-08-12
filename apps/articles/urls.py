from django.urls import path
from apps.articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index_articles'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page'),
    path('created_by/<int:_id>/',views.CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagListView.as_view(), name='tag'),
    path('search/', views.SearchListView.as_view(), name='search'),
]