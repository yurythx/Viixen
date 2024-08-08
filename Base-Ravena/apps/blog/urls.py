

from django.urls import path 
from blog import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'), 
    path('details/', views.blog_details, name='blog_details'),
]


