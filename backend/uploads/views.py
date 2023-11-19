from rest_framework import viewsets

from .models import AudioFile, ImageFile
from .serializers import AudioFileSerializer, ImageFileSerializer


class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

class ImageFileViewSet(viewsets.ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer