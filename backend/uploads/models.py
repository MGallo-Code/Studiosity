from django.db import models
import os
import uuid


def get_safe_image_path(instance, filename):
    get_safe_file_path(instance, filename, 'study_terms/images')

def get_safe_audio_path(instance, filename):
    get_safe_file_path(instance, filename, 'study_terms/audio')

def get_safe_file_path(instance, filename, extension):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/{extension}/', filename)

# AudioFile Model
class AudioFile(models.Model):
    """
    Represents an audio file associated with study materials.
    Stores the file path and upload timestamp of the audio file.
    """
    file_path = models.FileField(upload_to=get_safe_audio_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AudioFile {self.id}: {self.file_path.name}"

# ImageFile Model
class ImageFile(models.Model):
    """
    Represents an image file associated with study materials.
    Stores the file path and upload timestamp of the image file.
    """
    file_path = models.ImageField(upload_to=get_safe_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ImageFile {self.id}: {self.file_path.name}"