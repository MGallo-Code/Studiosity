from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import UserModel


class UserCreationSerializer(serializers.ModelSerializer):
    # Define a password field with write-only access and add Django's built-in password validators
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'password')  # Fields to be included in the serializer

    def create(self, validated_data):
        """
        Overrides the create method to create a new UserModel instance using the model manager.
        This ensures that the user is created with the hashed password and other model-specific logic.
        """
        return UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'bio', 'profile_image')
        extra_kwargs = {'username': {'required': False}, 'bio': {'required': False}}

    def update(self, instance, validated_data):
        """
        Overrides the update method to update an existing UserModel instance.
        Only the specified fields (username, bio, profile_image) are updated.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        if 'profile_image' in validated_data:
            instance.profile_image = validated_data.get('profile_image')
        instance.save()
        return instance

class UserPublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'profile_image', 'bio')  # Publicly accessible fields
    
    def to_representation(self, instance):
        """
        Override the to_representation method to customize the representation of the profile_image field.
        This method ensures the correct format and URL of the profile image is returned.
        """
        representation = super().to_representation(instance)
        # Provide the URL of the profile image if it exists, otherwise set it to None
        representation['profile_image'] = instance.profile_image.file_path.url if instance.profile_image else None
        return representation

# Serializer for the full profile of a user, excluding sensitive information like password
class UserFullProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('password',)  # Exclude password field from the serializer
        # Set fields that should not be modified directly via the API
        read_only_fields = ('email', 'is_validated', 'is_staff', 'is_superuser', 'created_at', 'updated_at')

    def to_representation(self, instance):
        """
        Override the to_representation method to customize the representation of the profile_image field.
        This method ensures the correct format and URL of the profile image is returned.
        """
        representation = super().to_representation(instance)
        # Provide the URL of the profile image if it exists, otherwise set it to None
        representation['profile_image'] = instance.profile_image.file_path.url if instance.profile_image else None
        return representation
