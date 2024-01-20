from django.db import models
from rest_framework import serializers

from uploads.models import AudioFile, ImageFile, TextToSpeechAudio
from .models import StudySet, Tag, StudyTerm


class StudySetSerializer(serializers.ModelSerializer):
    favorited = serializers.SerializerMethodField()

    class Meta:
        model = StudySet
        fields = ['id', 'title', 'description', 'uploader', 'private', 'created_at', 'favorited']
        read_only_fields = ['uploader', 'created_at', 'favorited']
        extra_kwargs = {
            "title": {"error_messages": {"required": "Please provide a set title"}},
        }

    def get_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorited_by.filter(user=user).exists()
        return False

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class StudyTermSerializer(serializers.ModelSerializer):
    # Helper method to create PrimaryKeyRelatedField for file fields
    def create_file_related_field(model, source):
        return serializers.PrimaryKeyRelatedField(
            queryset=model.objects.all(), 
            source=source, 
            write_only=True, 
            required=False, 
            allow_null=True
        )
    front_image_id = create_file_related_field(ImageFile, 'front_image')
    back_image_id = create_file_related_field(ImageFile, 'back_image')
    front_audio_id = create_file_related_field(AudioFile, 'front_audio')
    back_audio_id = create_file_related_field(AudioFile, 'back_audio')
    front_tts_audio_id = create_file_related_field(TextToSpeechAudio, 'front_tts_audio')
    back_tts_audio_id = create_file_related_field(TextToSpeechAudio, 'back_tts_audio')

    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = StudyTerm
        fields = ['id', 'sort_order',
                  'study_set',
                  'front_text',
                  'back_text',
                  'front_image',
                  'back_image',
                  'front_audio',
                  'back_audio',
                  'tags',
                  'front_image_id',
                  'back_image_id',
                  'front_audio_id',
                  'back_audio_id',
                  'front_voice_id',
                  'back_voice_id',
                  'front_tts_audio',
                  'back_tts_audio',
                  'front_tts_audio_id',
                  'back_tts_audio_id',
                  'created_at',
                  'updated_at']
    
    def to_representation(self, instance):
        """
        Override the to_representation method to customize the representation of the image and audio fields.
        """
        representation = super().to_representation(instance)
        # Process each file field and add URL to representation if the object exists
        for field_name in ['front_image', 'back_image', 'front_audio', 'back_audio', 'front_tts_audio', 'back_tts_audio']:
            file_obj = getattr(instance, field_name)
            representation[field_name] = {
                'id': file_obj.id,
                'file_path': file_obj.file.url
            } if file_obj else None
        return representation

    def update(self, instance, validated_data):
        # Handle the update of ImageFile and AudioFile references
        for field in ['front_image', 'back_image', 'front_audio', 'back_audio']:
            field_id = f'{field}_id'
            if field_id in validated_data:
                setattr(instance, field, validated_data.pop(field_id))
        return super().update(instance, validated_data)

class PublicStudyTermSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = StudyTerm
        fields = ['sort_order', 'front_text', 'back_text', 'front_image', 'back_image', 'front_audio', 'back_audio', 'tags']

    def to_representation(self, instance):
        """
        Override the to_representation method to customize the representation of the image and audio fields.
        """
        representation = super().to_representation(instance)
        # Process each file field and add URL to representation if the object exists
        for field_name in ['front_image', 'back_image', 'front_audio', 'back_audio', 'front_tts_audio', 'back_tts_audio']:
            file_obj = getattr(instance, field_name)
            representation[field_name] = {
                'file_path': file_obj.file.url
            } if file_obj else None
        return representation

class PublicSetsDetailSerializer(serializers.ModelSerializer):
    terms = PublicStudyTermSerializer(many=True, read_only=True)
    favorited = serializers.SerializerMethodField()

    class Meta:
        model = StudySet
        fields = ['id', 'title', 'description', 'uploader', 'created_at', 'favorited', 'terms']
        read_only_fields = ['uploader', 'created_at', 'favorited', 'terms']

    def get_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorited_by.filter(user=user).exists()
        return False