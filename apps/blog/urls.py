

from django.urls import path, re_path
from apps.blog import views

urlpatterns = [

    # The home page
    path('', views.index_blog, name='index_blog'),

   
]
