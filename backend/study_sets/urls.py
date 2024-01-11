from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteStudySetView, MySetsView, StudyTermViewSet, StudySetViewSet,
    UpdateSortOrderView, StudyTermsInSetView, PollyVoicesView, PublicSetsView, PublicSetDetailView
)


router = DefaultRouter()
router.register(r'terms', StudyTermViewSet, basename='study_term')
router.register(r'', StudySetViewSet, basename='study_set')

urlpatterns = [
    path('public_sets/<int:pk>/', PublicSetDetailView.as_view()),
    path('public_sets/', PublicSetsView.as_view()),
    path('my_sets/', MySetsView.as_view()),
    path('<int:pk>/terms/', StudyTermsInSetView.as_view()),
    path('get_voices/', PollyVoicesView.as_view()),
    path('<int:pk>/favorite/', FavoriteStudySetView.as_view()),
    path('<int:study_set_id>/update_term_order/', UpdateSortOrderView.as_view()),
    path('', include(router.urls)),
]
