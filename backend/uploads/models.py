from django.conf import settings
from django.db import models
import os
import uuid


def get_image_path(instance, filename):
    return safe_file_path(instance, filename, 'images')

def get_audio_path(instance, filename):
    return safe_file_path(instance, filename, 'audio')

def safe_file_path(instance, filename, extension):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(f'{extension}/', filename)

# AudioFile Model
class AudioFile(models.Model):
    """
    Represents an audio file associated with study materials.
    Stores the file path and upload timestamp of the audio file.
    """
    file_path = models.FileField(upload_to=get_audio_path, max_length=200)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_audio_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # delete the file from the filesystem
        if self.file_path:
            if os.path.isfile(self.file_path.path):
                os.remove(self.file_path.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"AudioFile {self.id}: {self.file_path.name}"

# ImageFile Model
class ImageFile(models.Model):
    """
    Represents an image file associated with study materials.
    Stores the file path and upload timestamp of the image file.
    """
    file_path = models.ImageField(upload_to=get_image_path, max_length=200)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_image_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # delete the file from the filesystem
        if self.file_path:
            if os.path.isfile(self.file_path.path):
                os.remove(self.file_path.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"ImageFile {self.id}: {self.file_path.name}"