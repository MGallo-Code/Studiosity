from rest_framework import serializers

from uploads.serializers import AudioFileSerializer, ImageFileSerializer
from .models import StudySet, Tag, StudyTerm


class StudySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySet
        fields = ['id', 'title', 'description', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class StudyTermSerializer(serializers.ModelSerializer):
    front_image = ImageFileSerializer(read_only=True)
    back_image = ImageFileSerializer(read_only=True)
    front_audio = AudioFileSerializer(read_only=True)
    back_audio = AudioFileSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = StudyTerm
        fields = ['id',
                 'study_set',
                 'front_text',
                 'back_text',
                 'front_image',
                 'back_image',
                 'front_audio',
                 'back_audio',
                 'tags',
                 'created_at']
