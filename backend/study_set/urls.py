from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'audio_file', views.AudioFileViewSet)
router.register(r'image_file', views.ImageFileViewSet)
router.register(r'set', views.StudySetViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'term', views.StudyTermViewSet)

urlpatterns = [
    path('', include(router.urls)),
]