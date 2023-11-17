from django.contrib import admin
from .models import StudySet, StudyTerm, Tag, StudyTermTag, AudioFile, ImageFile

admin.site.register(StudySet)
admin.site.register(StudyTerm)
admin.site.register(Tag)
admin.site.register(StudyTermTag)
admin.site.register(AudioFile)
admin.site.register(ImageFile)