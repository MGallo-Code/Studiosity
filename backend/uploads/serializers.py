from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import AudioFile, ImageFile


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