from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserModel
from .serializers import UserCreationSerializer, UserUpdateSerializer, UserPublicProfileSerializer, UserFullProfileSerializer


class IsOwnerOrSuperuser(BasePermission):
    """
    Custom permission to only allow owners of an object or superusers to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request user is the owner of the object or a superuser
        return obj == request.user or request.user.is_superuser

class GetAuthUserProfileView(APIView):
    """
    API endpoint for retrieving the authenticated user's full profile.
    Requires the user to be authenticated.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve and return the profile of the authenticated user.
        """
        user = request.user
        serializer = GetFullUserView(user)
        return Response(serializer.data)

class CreateUserView(generics.CreateAPIView):
    """
    API endpoint for creating a new user.
    No authentication required to create a new user.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserCreationSerializer

class UpdateUserView(generics.UpdateAPIView):
    """
    API endpoint for updating a user's profile.
    Only the user themselves or a superuser can update the profile.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserUpdateSerializer

    def get_permissions(self):
        """
        Override get_permissions to enforce custom permissions.
        """
        return [permissions.IsAuthenticated(), IsOwnerOrSuperuser()]

class GetPublicUserView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a user's public profile.
    No authentication required to view public profiles.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserPublicProfileSerializer
    lookup_field = 'username'  # We're using the username to retrieve the profile

class GetFullUserView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a user's full profile.
    Only the user themselves or a superuser can view the full profile.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserFullProfileSerializer
    lookup_field = 'username'  # Assume we're using the username to retrieve the profile

    def get_permissions(self):
        """
        Override get_permissions to enforce custom permissions.
        """
        return [permissions.IsAuthenticated(), IsOwnerOrSuperuser()]

class DeleteUserView(generics.DestroyAPIView):
    """
    API endpoint for deleting a user's profile.
    Only the user themselves or a superuser can delete the profile.
    """
    queryset = UserModel.objects.all()
    permission_classes = [IsOwnerOrSuperuser]
    lookup_field = 'id'

    def get_permissions(self):
        """
        Override get_permissions to enforce custom permissions.
        """
        return [permissions.IsAuthenticated(), IsOwnerOrSuperuser()]
