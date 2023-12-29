from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import AudioFile, ImageFile, TextToSpeechAudio


MAX_IMG_SIZE = 20971520
MAX_AUDIO_SIZE = 20971520

class TextToSpeechAudioSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)
    
    class Meta:
        model = TextToSpeechAudio
        fields = ['id', 'audio_file', 'uploader', 'created_at']
        read_only_fields = ['id', 'created_at', 'uploader']

class AudioFileSerializer(serializers.ModelSerializer):
    def validate_file_path(self, value):
        if not value.name.lower().endswith(('.wav', '.mp3', '.ogg')):
            raise ValidationError("Unsupported audio file type.")
        elif value.size > MAX_AUDIO_SIZE:
            raise ValidationError(f"File size should not exceed {MAX_AUDIO_SIZE/1048576} MB.")
        return value
    class Meta:
        model = AudioFile
        fields = ['id', 'file', 'uploaded_at', 'uploader']
        read_only_fields = ['uploaded_at', 'uploader']

class ImageFileSerializer(serializers.ModelSerializer):
    def validate_file_path(self, value):
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Unsupported image file type.")
        elif value.size > MAX_IMG_SIZE:
            raise ValidationError(f"File size should not exceed {MAX_IMG_SIZE/1048576} MB.")
        return value

    class Meta:
        model = ImageFile
        fields = ['id', 'file', 'uploaded_at', 'uploader']
        read_only_fields = ['uploaded_at', 'uploader']