from django.urls import path

from .views import UserRegistrationView, UserProfileView, UserUpdateView, LoginView, CurrentUserProfileView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
]