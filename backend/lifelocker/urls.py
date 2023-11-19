from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('study_sets/', include("study_sets.urls")),
    path('uploads/', include("uploads.urls"))
]
