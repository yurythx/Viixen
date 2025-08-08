from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('modules.accounts.urls')),
    path('config/', include('modules.config.urls')),
    path('pages/', include('modules.pages.urls')),
    path('blog/', include('modules.blog.urls')),
    path('', include('modules.pages.urls', namespace='home')),  # Usar namespace diferente
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
