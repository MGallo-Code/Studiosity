from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import AudioFile, ImageFile, TextToSpeechAudio


# Define maximum file sizes for images and audio files
MAX_IMG_SIZE = 20971520 # 20 MB
MAX_AUDIO_SIZE = 20971520 # 20 MB

class TextToSpeechAudioSerializer(serializers.ModelSerializer):
    # Declaring a FileField for the 'file' attribute, setting it as not required.
    # This allows creating a TextToSpeechAudio object without initially providing a file.
    # The file is expected to be generated and saved immediately afterward.
    file = serializers.FileField(required=False)
    
    class Meta:
        model = TextToSpeechAudio
        fields = ['id', 'file', 'uploader', 'created_at']
        read_only_fields = ['id', 'created_at', 'uploader']

class AudioFileSerializer(serializers.ModelSerializer):
    # Custom validation for the 'file' field.
    # Ensures the file is of an acceptable audio format and within size limits.
    def validate_file(self, value):
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
    # Custom validation for the 'file' field.
    # Ensures the file is of an acceptable image format and within size limits.
    def validate_file(self, value):
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Unsupported image file type.")
        elif value.size > MAX_IMG_SIZE:
            raise ValidationError(f"File size should not exceed {MAX_IMG_SIZE/1048576} MB.")
        return value
    class Meta:
        model = ImageFile
        fields = ['id', 'file', 'uploaded_at', 'uploader']
        read_only_fields = ['uploaded_at', 'uploader']