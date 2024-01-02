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

    def get_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorited_by.filter(user=user).exists()
        return False

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ReorderStudyTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyTerm
        fields = ['id', 'sort_order']

    def update_ordering(self, instance, validated_data):
        # Get the new and old positions
        new_order = validated_data.get('sort_order')
        old_order = instance.sort_order

        if new_order > old_order:
            # Shift terms between the old and new positions back by one
            StudyTerm.objects.filter(
                study_set=instance.study_set,
                sort_order__gt=old_order,
                sort_order__lte=new_order
            ).update(sort_order=models.F('sort_order') - 1)
        else:
            # Shift terms between the new and old positions forward by one
            StudyTerm.objects.filter(
                study_set=instance.study_set,
                sort_order__lt=old_order,
                sort_order__gte=new_order
            ).update(sort_order=models.F('sort_order') + 1)

        # Update the moved term's sort_order
        instance.sort_order = new_order
        instance.save()

        return instance

    def update(self, instance, validated_data):
        return self.update_ordering(instance, validated_data)


class StudyTermSerializer(serializers.ModelSerializer):
    # Accept IDs for related objects
    front_image_id = serializers.PrimaryKeyRelatedField(
        queryset=ImageFile.objects.all(), 
        source='front_image', 
        write_only=True, 
        required=False,
        allow_null=True
    )
    back_image_id = serializers.PrimaryKeyRelatedField(
        queryset=ImageFile.objects.all(), 
        source='back_image', 
        write_only=True, 
        required=False,
        allow_null=True
    )
    front_audio_id = serializers.PrimaryKeyRelatedField(
        queryset=AudioFile.objects.all(), 
        source='front_audio', 
        write_only=True, 
        required=False,
        allow_null=True
    )
    back_audio_id = serializers.PrimaryKeyRelatedField(
        queryset=AudioFile.objects.all(), 
        source='back_audio', 
        write_only=True, 
        required=False,
        allow_null=True
    )
    front_tts_audio_id = serializers.PrimaryKeyRelatedField(
        queryset=TextToSpeechAudio.objects.all(),
        source='front_tts_audio',
        write_only=True,
        required=False,
        allow_null=True
    )
    back_tts_audio_id = serializers.PrimaryKeyRelatedField(
        queryset=TextToSpeechAudio.objects.all(),
        source='back_tts_audio',
        write_only=True,
        required=False,
        allow_null=True
    )
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
        read_only_fields = ['sort_order', 'front_image', 'back_image', 'front_audio', 'back_audio']
    
    def to_representation(self, instance):
        """
        Override the to_representation method to customize the representation of the image and audio fields.
        """
        representation = super().to_representation(instance)

        # Process each field and add URL to representation if the object exists
        for field_name in ['front_image', 'back_image', 'front_audio', 'back_audio', 'front_tts_audio', 'back_tts_audio']:
            field_instance = getattr(instance, field_name)
            if field_instance:
                representation[field_name] = {
                    'id': field_instance.id,
                    'file_path': field_instance.file.url
                }
            else:
                representation[field_name] = None

        return representation

    def update(self, instance, validated_data):
        # Handle the update of ImageFile and AudioFile references
        for field in ['front_image', 'back_image', 'front_audio', 'back_audio']:
            if f'{field}_id' in validated_data:
                setattr(instance, field, validated_data.pop(f'{field}_id'))

        return super().update(instance, validated_data)