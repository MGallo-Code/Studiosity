from django.urls import path
from .views import IsAuthorizedView, AllUsersView, GetAuthUserProfileView, CreateUserView, DeleteUserView, UpdateUserView, GetPublicUserView

app_name = 'users'

urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('is_authorized/', IsAuthorizedView.as_view()),
    path('profile/<str:username>/', GetPublicUserView.as_view()),
    path('profile/', GetAuthUserProfileView.as_view()),
    path('update/<int:pk>/', UpdateUserView.as_view()),
    path('delete/<int:pk>/', DeleteUserView.as_view()),
    path('all_users/', AllUsersView.as_view())
]