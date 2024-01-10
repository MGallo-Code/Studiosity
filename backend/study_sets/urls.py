from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteStudySetView, MySetsView, StudyTermViewSet, StudySetViewSet,
    UpdateSortOrderView, StudyTermsInSetView, PollyVoicesView
)


router = DefaultRouter()
router.register(r'terms', StudyTermViewSet, basename='study_term')
router.register(r'', StudySetViewSet, basename='study_set')

urlpatterns = [
    path('my_sets/', MySetsView.as_view()),
    path('<int:pk>/terms/', StudyTermsInSetView.as_view()),
    path('get_voices/', PollyVoicesView.as_view()),
    path('<int:pk>/favorite/', FavoriteStudySetView.as_view()),
    path('<int:study_set_id>/update_term_order/', UpdateSortOrderView.as_view()),
    path('', include(router.urls)),
]
