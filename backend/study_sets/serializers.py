from rest_framework import serializers

from uploads.models import AudioFile, ImageFile
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

class StudyTermSerializer(serializers.ModelSerializer):
    # Accept IDs for related objects
    front_image_id = serializers.PrimaryKeyRelatedField(
        queryset=ImageFile.objects.all(), 
        source='front_image', 
        write_only=True, 
        required=False
    )
    back_image_id = serializers.PrimaryKeyRelatedField(
        queryset=ImageFile.objects.all(), 
        source='back_image', 
        write_only=True, 
        required=False
    )
    front_audio_id = serializers.PrimaryKeyRelatedField(
        queryset=AudioFile.objects.all(), 
        source='front_audio', 
        write_only=True, 
        required=False
    )
    back_audio_id = serializers.PrimaryKeyRelatedField(
        queryset=AudioFile.objects.all(), 
        source='back_audio', 
        write_only=True, 
        required=False
    )
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
                  'front_image_id',
                  'back_image_id',
                  'front_audio_id',
                  'back_audio_id',
                  'created_at',
                  'updated_at']
        read_only_fields = ['front_image', 'back_image', 'front_audio', 'back_audio']

    def update(self, instance, validated_data):
        # Handle the update of ImageFile and AudioFile references
        for field in ['front_image', 'back_image', 'front_audio', 'back_audio']:
            if f'{field}_id' in validated_data:
                setattr(instance, field, validated_data.pop(f'{field}_id'))

        return super().update(instance, validated_data)