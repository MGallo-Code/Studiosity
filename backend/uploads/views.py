from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from .models import AudioFile, ImageFile
from .serializers import AudioFileSerializer, ImageFileSerializer


class IsUploaderOrSuperuser(BasePermission):
    """
    Custom permission to only allow the uploader of a file or a superuser to delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the uploader of the file or a superuser.
        return obj.uploader == request.user or request.user.is_superuser

class AudioFileViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class ImageFileViewSet(mixins.CreateModelMixin, 
                       mixins.DestroyModelMixin, 
                       viewsets.GenericViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)