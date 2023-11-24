from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MyStudySetsView, PublicStudySetsView, AllStudySetsView, 
    StudySetViewSet, CreateStudySetView, StudyTermsInSetView, TagViewSet
)


router = DefaultRouter()
router.register(r'sets', StudySetViewSet, basename='study_set')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('my_sets/', MyStudySetsView.as_view(), name='my_study_sets'),
    path('public_sets/', PublicStudySetsView.as_view(), name='public_study_sets'),
    path('all_sets/', AllStudySetsView.as_view(), name='all_study_sets'),
    path('create_set/', CreateStudySetView.as_view(), name='create_study_set'),
    path('terms_in_set/<int:pk>/', StudyTermsInSetView.as_view(), name='terms_in_set'),
    path('', include(router.urls)),
]
