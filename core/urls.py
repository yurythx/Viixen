
from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD nova Routes AQUI

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),
    path("config/", include("apps.config.urls")),
    path("blog/", include("apps.blog.urls")),
    
]
