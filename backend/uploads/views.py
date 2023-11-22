from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import AudioFile, ImageFile
from .serializers import AudioFileSerializer, ImageFileSerializer


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