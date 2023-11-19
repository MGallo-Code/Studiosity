from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StudySetViewSet, StudyTermViewSet, TagViewSet


router = DefaultRouter()
router.register(r'sets', StudySetViewSet)
router.register(r'terms', StudyTermViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]