from django.urls import path
from .views import AudioFileCreateView, AudioFileDeleteView, ImageFileCreateView, ImageFileDeleteView

app_name = 'uploads'

urlpatterns = [
    path('images/', ImageFileCreateView.as_view(), name='image-file-create'),
    path('images/<str:pk>/', ImageFileDeleteView.as_view(), name='image-file-delete'),
    path('audio/', AudioFileCreateView.as_view(), name='audio-file-create'),
    path('audio/<str:pk>/', AudioFileDeleteView.as_view(), name='audio-file-delete'),
]