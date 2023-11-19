from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AudioFileViewSet, ImageFileViewSet


router = DefaultRouter()
router.register(r'audio_files', AudioFileViewSet)
router.register(r'image_files', ImageFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]