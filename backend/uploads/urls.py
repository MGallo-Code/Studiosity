from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AudioFileViewSet, ImageFileViewSet


router = DefaultRouter()
router.register(r'audio', AudioFileViewSet)
router.register(r'images', ImageFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]