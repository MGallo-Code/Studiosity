from django.conf import settings
from django.db import models
import os
import uuid

def get_image_path(instance, filename):
    """
    Generate a path for saving an image file.
    The filename is generated using a UUID to ensure uniqueness.
    """
    return safe_file_path(instance, filename, 'images')

def get_audio_path(instance, filename):
    """
    Generate a path for saving an audio file.
    The filename is generated using a UUID to ensure uniqueness.
    """
    return safe_file_path(instance, filename, 'audio')

def safe_file_path(instance, filename, extension):
    """
    Create a safe file path by appending a UUID to the filename.
    This prevents filename collisions when saving files.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(f'{extension}/', filename)

class AudioFile(models.Model):
    """
    AudioFile Model: Represents an audio file.
    - file_path: Stores the path to the audio file. The path is generated using get_audio_path.
    - uploader: ForeignKey to the User model, represents the user who uploaded the file.
    - uploaded_at: The date and time when the file was uploaded.
    """
    file_path = models.FileField(upload_to=get_audio_path, max_length=200)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_audio_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """
        Overridden delete method to remove the file from the filesystem upon deletion of the database record.
        """
        if self.file_path and os.path.isfile(self.file_path.path):
            os.remove(self.file_path.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"AudioFile {self.id}: {self.file_path.name}"

class ImageFile(models.Model):
    """
    ImageFile Model: Represents an image file.
    - file_path: Stores the path to the image file. The path is generated using get_image_path.
    - uploader: ForeignKey to the User model, represents the user who uploaded the file.
    - uploaded_at: The date and time when the file was uploaded.
    """
    file_path = models.ImageField(upload_to=get_image_path, max_length=200)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_image_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """
        Overridden delete method to remove the file from the filesystem upon deletion of the database record.
        """
        if self.file_path and os.path.isfile(self.file_path.path):
            os.remove(self.file_path.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"ImageFile {self.id}: {self.file_path.name}"