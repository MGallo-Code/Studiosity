from django.db import models

# StudySet Model
class StudySet(models.Model):
    pk_study_set_id = models.AutoField(primary_key=True)
    set_title = models.CharField(max_length=64)
    set_description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# StudyTerm Model
class StudyTerm(models.Model):
    pk_term_id = models.AutoField(primary_key=True)
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE, related_name='study_terms')
    front_text = models.TextField(blank=True, default='Front')
    back_text = models.TextField(blank=True, default='Back')
    # Foreign keys for image and audio will be added later
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Tag Model
class Tag(models.Model):
    pk_tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=16)

# StudyTermTag Model
class StudyTermTag(models.Model):
    study_term = models.ForeignKey(StudyTerm, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

# AudioFile Model
class AudioFile(models.Model):
    pk_audio_file_id = models.AutoField(primary_key=True)
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# ImageFile Model
class ImageFile(models.Model):
    pk_image_file_id = models.AutoField(primary_key=True)
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Adding the foreign key relationships to StudyTerm for Audio and Image files
StudyTerm.add_to_class('fk_front_image', models.ForeignKey(ImageFile, on_delete=models.SET_NULL, null=True, blank=True, related_name='front_terms'))
StudyTerm.add_to_class('fk_back_image', models.ForeignKey(ImageFile, on_delete=models.SET_NULL, null=True, blank=True, related_name='back_terms'))
StudyTerm.add_to_class('fk_front_audio', models.ForeignKey(AudioFile, on_delete=models.SET_NULL, null=True, blank=True, related_name='front_audio_terms'))
StudyTerm.add_to_class('fk_back_audio', models.ForeignKey(AudioFile, on_delete=models.SET_NULL, null=True, blank=True, related_name='back_audio_terms'))
