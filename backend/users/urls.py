from django.urls import path
from .views import AuthenticatedUserProfileView, CreateUserView, UpdateUserView, UserPublicProfileView, UserFullProfileView

app_name = 'users'  # It's a good practice to use app_name for namespacing in Django apps

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('update/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('public/<str:username>/', UserPublicProfileView.as_view(), name='public_profile'),
    path('profile/', AuthenticatedUserProfileView.as_view(), name='authenticated_user_profile'),
    path('profile/<str:username>/', UserFullProfileView.as_view(), name='full_profile'),
]