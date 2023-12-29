from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AudioFileViewSet, ImageFileViewSet

app_name = 'uploads'

router = DefaultRouter()
router.register(r'audio', AudioFileViewSet, basename='audio_file')
router.register(r'images', ImageFileViewSet, basename='image_file')

urlpatterns = [
    path('', include(router.urls)),
]
