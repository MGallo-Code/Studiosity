from rest_framework import serializers
from .models import AudioFile, ImageFile, StudySet, Tag, StudyTerm
from django.core.exceptions import ValidationError

MAX_IMG_SIZE = 10485760
MAX_AUDIO_SIZE = 10485760

class AudioFileSerializer(serializers.ModelSerializer):
    def validate_file_path(self, value):
        if not value.name.lower().endswith(('.wav', '.mp3', '.ogg')):
            raise ValidationError("Unsupported audio file type.")
        elif value.size > MAX_AUDIO_SIZE:
            raise ValidationError(f"File size should not exceed {MAX_AUDIO_SIZE/1048576} MB.")
        return value
    class Meta:
        model = AudioFile
        fields = ['id', 'file_path']

class ImageFileSerializer(serializers.ModelSerializer):
    def validate_file_path(self, value):
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Unsupported image file type.")
        elif value.size > MAX_IMG_SIZE:
            raise ValidationError(f"File size should not exceed {MAX_IMG_SIZE/1048576} MB.")
        return value

    class Meta:
        model = ImageFile
        fields = ['id', 'file_path']

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
        field = ['id',
                 'study_set',
                 'front_text',
                 'back_text',
                 'front_image',
                 'back_image',
                 'front_audio',
                 'back_audio',
                 'tags',
                 'created_at']
