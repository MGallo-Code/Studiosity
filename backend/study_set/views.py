from rest_framework import viewsets

from .serializers import AudioFileSerializer, ImageFileSerializer, StudySetSerializer, TagSerializer, StudyTermSerializer
from .models import AudioFile, ImageFile, StudySet, Tag, StudyTerm

class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

class ImageFileViewSet(viewsets.ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer

class StudySetViewSet(viewsets.ModelViewSet):
    queryset = StudySet.objects.all()
    serializer_class = StudySetSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class StudyTermViewSet(viewsets.ModelViewSet):
    queryset = StudyTerm.objects.all()
    serializer_class = StudyTermSerializer