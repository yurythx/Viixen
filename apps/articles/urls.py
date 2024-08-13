from django.urls import path
from apps.articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='index_articles'),
    #path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    
    path('articles/<slug:slug>/', views.ArticleDetails.as_view(), name='article-details'),
     
    path('created_by/<int:_id>/',views.CreatedByListView.as_view(), name='created_by'),
    path('new-article/<int:_id>/',views.ArticleCreate.as_view(), name='new-article'),
    path('update-article/<int:pk>', views.ArticleUpdateView.as_view(), name='update-article'),
    path('delete-article/<int:pk>', views.ArticleDeleteView.as_view(), name='delete-article'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagListView.as_view(), name='tag'),
    path('search/', views.SearchListView.as_view(), name='search'),
]