from rest_framework import status, generics, views
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from uploads.models import ImageFile
from .models import UserModel
from .serializers import UserCreationSerializer, UserUpdateSerializer, UserPublicProfileSerializer, UserFullProfileSerializer


class IsSuperuser(BasePermission):
    """
    Custom permission class to allow access only to superusers.
    """

    def has_permission(self, request, view):
        # Check if the request user is the owner of the object or a superuser
        return request.user.is_superuser

class IsUserOwnerOrSuperuser(BasePermission):
    """
    Custom permission to only allow owners of an object or superusers to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request user is the owner of the object or a superuser
        return obj == request.user or request.user.is_superuser

class IsAuthorizedView(views.APIView):
    """
    API view to check if the user is authenticated.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # If the request reaches here, the user is authenticated
        return Response({
            'message': 'User is authenticated',
        }, status=status.HTTP_200_OK)

class GetAuthUserProfileView(views.APIView):
    """
    API endpoint for retrieving the authenticated user's full profile.
    Requires the user to be authenticated.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve and return the profile of the authenticated user.
        """
        user = request.user
        serializer = UserFullProfileSerializer(user)
        return Response(serializer.data)

class CreateUserView(generics.CreateAPIView):
    """
    API endpoint for creating a new user.
    No authentication required to create a new user.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = []

class UpdateUserView(generics.UpdateAPIView):
    """
    API endpoint for updating a user's profile.
    Only the user themselves or a superuser can update the profile.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsUserOwnerOrSuperuser]

    def perform_update(self, serializer):
        user = self.get_object()
        new_profile_image_id = self.request.data.get('profile_image')

        if new_profile_image_id:
            try:
                new_profile_image = ImageFile.objects.get(pk=new_profile_image_id)
            except ImageFile.DoesNotExist:
                raise PermissionDenied(detail=f"Referenced ImageFile with ID: {new_profile_image_id} does not exist.")

            if new_profile_image.uploader != self.request.user and not user.is_superuser:
                raise PermissionDenied(detail="You do not have permission to use this image.")

            # Check for and delete the old profile image if necessary
            if new_profile_image and user.profile_image and user.profile_image.id != new_profile_image:
                user.profile_image.delete()

        # Call save on the serializer for other updates (like username)
        serializer.save()

class GetPublicUserView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a user's public profile.
    No authentication required to view public profiles.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserPublicProfileSerializer
    lookup_field = 'username'  # We're using the username to retrieve the profile

class DeleteUserView(generics.DestroyAPIView):
    """
    API endpoint for deleting a user's profile.
    Only the user themselves or a superuser can delete the profile.
    """
    queryset = UserModel.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwnerOrSuperuser]

class AllUsersView(generics.ListAPIView):
    serializer_class = UserFullProfileSerializer
    permission_classes = [IsSuperuser]

    def get_queryset(self):
        """
        This view returns a list of all the study sets.
        Admin privilege required.
        """
        return UserModel.objects.all()
