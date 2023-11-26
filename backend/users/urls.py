from django.urls import path
from .views import AllUsersView, GetAuthUserProfileView, CreateUserView, DeleteUserView, UpdateUserView, GetPublicUserView

app_name = 'users'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('profile/<str:username>/', GetPublicUserView.as_view(), name='public_profile'),
    path('profile/', GetAuthUserProfileView.as_view(), name='authenticated_user_profile'),
    path('update/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('delete/<int:id>/', DeleteUserView.as_view(), name='delete_user'),
    path('all_users/', AllUsersView.as_view(), name='all_users')
]