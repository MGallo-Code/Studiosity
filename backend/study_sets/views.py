from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import AudioFileSerializer, ImageFileSerializer, StudySetSerializer, TagSerializer, StudyTermSerializer
from .models import AudioFile, ImageFile, StudySet, Tag, StudyTerm

class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

class ImageFileViewSet(viewsets.ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer

# URL pattern(s):
#  /study_sets/
#    - All study sets
#  /study_sets/<pk>
#    - Study set with id=pk
class StudySetViewSet(viewsets.ModelViewSet):
    queryset = StudySet.objects.all()
    serializer_class = StudySetSerializer

    # URL: /study_sets/<pk>/terms/
    # Retrieve study terms related to a specific study set
    @action(detail=True, methods=['get'])
    def terms(self, request, pk=None):
        study_set = self.get_object()
        terms = study_set.study_terms.all()
        serializer = StudyTermSerializer(terms, many=True)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class StudyTermViewSet(viewsets.ModelViewSet):
    queryset = StudyTerm.objects.all()
    serializer_class = StudyTermSerializer