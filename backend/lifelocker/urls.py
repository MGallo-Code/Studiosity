from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/users/', include("users.urls")),
    path('api/study_sets/', include("study_sets.urls")),
    path('api/uploads/', include("uploads.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
