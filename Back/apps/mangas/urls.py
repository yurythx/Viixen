from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MangaViewSet, ChapterViewSet, PageViewSet,
    UserStatisticsViewSet, MangaViewViewSet
)
from .chunked_upload import ChunkedUploadView

router = DefaultRouter()
router.register(r'mangas', MangaViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'pages', PageViewSet)
router.register(r'statistics', UserStatisticsViewSet)
router.register(r'history', MangaViewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chunked-upload/', ChunkedUploadView.as_view(), name='chunked-upload'),
]
