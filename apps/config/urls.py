
from django.urls import path, re_path
from apps.config import views

urlpatterns = [

    # The home page
    path('', views.index_config, name='index_config'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages_config, name='pages_config'),

]
