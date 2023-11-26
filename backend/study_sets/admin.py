from django.contrib import admin
from .models import StudySet, StudyTerm, Tag

admin.site.register(StudySet)
admin.site.register(StudyTerm)
admin.site.register(Tag)