
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD nova Routes AQUI

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),
    path("config/", include("apps.config.urls")),
    path("articles/", include("apps.articles.urls")),
   

    
    path('tinymce/', include('tinymce.urls')),
    
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )