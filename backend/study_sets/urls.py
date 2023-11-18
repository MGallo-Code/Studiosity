from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.StudySetViewSet)
router.register(r'terms', views.StudyTermViewSet)
router.register(r'audio_files', views.AudioFileViewSet)
router.register(r'image_files', views.ImageFileViewSet)
router.register(r'tags', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]