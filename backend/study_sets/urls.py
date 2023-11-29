from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MyStudySetsView, StudyTermViewSet, StudySetViewSet,
    StudyTermsInSetView, TagViewSet
)


router = DefaultRouter()
router.register(r'study_sets', StudySetViewSet, basename='study_set')
router.register(r'study_terms', StudyTermViewSet, basename='study_term')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('my_sets/', MyStudySetsView.as_view(), name='my_study_sets'),
    path('terms_in_set/<int:pk>/', StudyTermsInSetView.as_view(), name='terms_in_set'),
    path('', include(router.urls)),
]
