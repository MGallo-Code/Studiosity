from django.db import models
from django.db.models import Max
from django.conf import settings

from users.models import UserModel
from uploads.models import AudioFile, ImageFile, TextToSpeechAudio


# StudySet Model
class StudySet(models.Model):
    """
    Represents a set of study materials.
    Contains information about the study set including title, description,
    and timestamps for creation and last update.
    """
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')
    private = models.BooleanField(default=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_sets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Study Set {self.id}: {self.title}"

# Tag Model
class Tag(models.Model):
    """
    Represents a tag for categorizing study terms.
    Each tag has a unique name.
    """
    name = models.CharField(max_length=16, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return f"Tag {self.id}: {self.name}"


# StudyTerm Model
class StudyTerm(models.Model):
    """
    Represents a study term within a study set.
    Includes text for the front and back, optional associated image and audio files,
    and a set of tags for categorization. Also tracks creation and update times.
    """
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE, related_name='study_terms')
    sort_order = models.IntegerField(null=True, blank=True)
    front_text = models.TextField(blank=True, default='Front')
    back_text = models.TextField(blank=True, default='Back')
    front_image = models.OneToOneField(
        ImageFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='front_image_study_term'
    )
    back_image = models.OneToOneField(
        ImageFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='back_image_study_term'
    )
    front_audio = models.OneToOneField(
        AudioFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='front_audio_study_term'
    )
    back_audio = models.OneToOneField(
        AudioFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='back_audio_study_term'
    )
    # AWS Polly Voice ID
    front_voice_id = models.CharField(default="Joanna", max_length=100, blank=False, null=False)
    back_voice_id = models.CharField(default="Joanna", max_length=100, blank=False, null=False)
    # TTS Audio Files
    front_tts_audio = models.OneToOneField(
        TextToSpeechAudio, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='front_tts_study_term'
    )
    back_tts_audio = models.OneToOneField(
        TextToSpeechAudio, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='back_tts_study_term'
    )
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensure a unique sort_order within the same study_set
        unique_together = [['study_set', 'sort_order']]

    def save(self, *args, **kwargs):
        if self._state.adding and self.sort_order is None:
            last_sort_order = StudyTerm.objects.aggregate(Max('sort_order'))['sort_order__max'] or 0
            self.sort_order = last_sort_order + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Overridden delete method to remove the associated images
        from the filesystem and database upon deletion of the study term.
        """
        if hasattr(self, 'front_image') and self.front_image:
            self.front_image.delete()
        if hasattr(self, 'back_image') and self.back_image:
            self.back_image.delete()

        if hasattr(self, 'front_audio') and self.front_audio:
            self.front_audio.delete()
        if hasattr(self, 'back_audio') and self.back_audio:
            self.back_audio.delete()
        
        if hasattr(self, 'front_tts_audio') and self.front_tts_audio:
            self.front_tts_audio.delete()
        if hasattr(self, 'back_tts_audio') and self.back_tts_audio:
            self.back_tts_audio.delete()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Term {self.id}: {self.front_text} | {self.back_text}"

class Favorite(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='favorites')
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'study_set')

    def __str__(self):
        return f"{self.user.username} favorited {self.study_set.title}"