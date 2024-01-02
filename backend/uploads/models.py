from django.conf import settings
from django.db import models
import os
import uuid

def get_image_path(instance, filename):
    """
    Create a safe file path by appending a UUID to the filename.
    This prevents filename collisions when saving files.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(f'images/', filename)


def get_audio_path(instance, filename):
    """
    Generate a path for saving an audio file using a UUID for uniqueness.
    """
    ext = filename.split('.')[-1]
    # Ensure the file is saved in the 'audio' directory with a unique name
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(f'audio/', filename)

def get_tts_audio_path(instance, filename):
    """
    Generate a path for saving a tts audio file using a UUID for uniqueness.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'tts_audio/{filename}'

class TextToSpeechAudio(models.Model):
    """
    TextToSpeechAudio Model: Represents an audio file generated from text.
    """
    file = models.FileField(upload_to=get_tts_audio_path)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='text_to_speech_audios'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def delete(self, *args, **kwargs):
        """
        Overridden delete method to remove the file from the filesystem upon deletion of the database record.
        """
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"TextToSpeechAudio {self.id} - Uploaded by {self.uploader}"

class AudioFile(models.Model):
    file = models.FileField(upload_to=get_audio_path, max_length=200)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_audio_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """
        Overridden delete method to remove the file from the filesystem upon deletion of the database record.
        """
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"AudioFile {self.id}: {self.file.name}"

class ImageFile(models.Model):
    """
    ImageFile Model: Represents an image file.
    - file: Stores the image file. The path is generated using get_image_path.
    - uploader: ForeignKey to the User model, represents the user who uploaded the file.
    - uploaded_at: The date and time when the file was uploaded.
    """
    file = models.ImageField(upload_to=get_image_path, max_length=200)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_image_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """
        Overridden delete method to remove the file from the filesystem upon deletion of the database record.
        """
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"ImageFile {self.id}: {self.file.name}"