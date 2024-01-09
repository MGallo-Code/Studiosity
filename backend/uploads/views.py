from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AudioFile, ImageFile
from .serializers import AudioFileSerializer, ImageFileSerializer


class IsUploaderOrSuperuser(BasePermission):
    """
    Custom permission to only allow the uploader of a file or a superuser to delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed to the uploader of the file or a superuser.
        return obj.uploader == request.user or request.user.is_superuser


class ImageFileCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        Handle POST request to create a new image file.

        Returns:
        - Response: An HTTP response object. Returns 201 Created status on success
          with the serialized image file data. Returns 400 Bad Request status on failure
          with error details.
        """
        serializer = ImageFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploader=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageFileDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsUploaderOrSuperuser]

    def delete(self, request, pk, format=None):
        """
        Handle DELETE request to delete an image file.

        Returns:
        - Response: An HTTP response object. Returns 204 No Content status on successful
          deletion. Returns 404 Not Found status if the image file does not exist.
          Returns 403 Forbidden if the user does not have permission to delete the file.
        """
        try:
            image_file = ImageFile.objects.get(pk=pk)
        except ImageFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, image_file)
        image_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AudioFileCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        Handle POST request to create a new audio file.

        Returns:
        - Response: An HTTP response object. Returns 201 Created status on success
          with the serialized audio file data. Returns 400 Bad Request status on failure
          with error details.
        """
        serializer = AudioFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploader=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AudioFileDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsUploaderOrSuperuser]

    def delete(self, request, pk, format=None):
        """
        Handle DELETE request to delete an audio file.

        Returns:
        - Response: An HTTP response object. Returns 204 No Content status on successful
          deletion. Returns 404 Not Found status if the audio file does not exist.
          Returns 403 Forbidden if the user does not have permission to delete the file.
        """
        try:
            audio_file = AudioFile.objects.get(pk=pk)
        except AudioFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, audio_file)
        audio_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)