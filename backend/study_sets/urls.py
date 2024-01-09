from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteStudySetView, MyStudySetsView, StudyTermViewSet, StudySetViewSet,
    UpdateSortOrderView, StudyTermsInSetView, TagViewSet, PollyVoicesView
)


router = DefaultRouter()
router.register(r'study_sets', StudySetViewSet, basename='study_set')
router.register(r'study_terms', StudyTermViewSet, basename='study_term')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('my_sets/', MyStudySetsView.as_view(), name='my_study_sets'),
    path('terms_in_set/<int:pk>/', StudyTermsInSetView.as_view(), name='terms_in_set'),
    path('get_voices/', PollyVoicesView.as_view(), name='get_voices'),
    path('update_term_order/<int:study_set_id>/', UpdateSortOrderView.as_view(), name='update_sort_order'),
    path('favorite/<int:pk>/', FavoriteStudySetView.as_view(), name='favorite_study_set'),
    path('', include(router.urls)),
]
