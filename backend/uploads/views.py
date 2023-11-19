from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from .models import AudioFile, ImageFile
from .serializers import AudioFileSerializer, ImageFileSerializer


class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    parser_classes = (MultiPartParser, FormParser)

class ImageFileViewSet(viewsets.ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer
    parser_classes = (MultiPartParser, FormParser)