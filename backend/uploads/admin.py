from django.contrib import admin

from .models import AudioFile, ImageFile


admin.site.register(AudioFile)
admin.site.register(ImageFile)