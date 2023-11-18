from django.contrib import admin
from .models import StudySet, StudyTerm, Tag, AudioFile, ImageFile

admin.site.register(StudySet)
admin.site.register(StudyTerm)
admin.site.register(Tag)
admin.site.register(AudioFile)
admin.site.register(ImageFile)