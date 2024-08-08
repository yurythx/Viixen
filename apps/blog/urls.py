

from django.urls import path, re_path
from apps.blog import views

urlpatterns = [

    # The home page
    path('', views.blog_index, name='blog_index'),

   
]
