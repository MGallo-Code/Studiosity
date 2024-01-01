from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .authentication import CustomTokenObtainPairView, CustomTokenRefreshView, logout_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', logout_view, name='logout'),
    path('api/users/', include("users.urls")),
    path('api/study_sets/', include("study_sets.urls")),
    path('api/uploads/', include("uploads.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
