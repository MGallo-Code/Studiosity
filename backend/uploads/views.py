import uuid
from boto3 import Session
from django.core.files.base import ContentFile
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response

from .models import AudioFile, ImageFile, TextToSpeechAudio
from .serializers import AudioFileSerializer, ImageFileSerializer, TextToSpeechAudioSerializer


class IsUploaderOrSuperuser(BasePermission):
    """
    Custom permission to only allow the uploader of a file or a superuser to delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the uploader of the file or a superuser.
        return obj.uploader == request.user or request.user.is_superuser

class TextToSpeechAudioViewSet(viewsets.ModelViewSet):
    queryset = TextToSpeechAudio.objects.all()
    serializer_class = TextToSpeechAudioSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        text = request.data.get('text')
        if not text:
            return Response({"error": "Field 'text' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize AWS Polly client and synthesize speech
        polly = Session(region_name='us-east-2').client('polly')
        response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')

        if "AudioStream" in response:
            audio_content = ContentFile(response['AudioStream'].read())
            filename = f"{uuid.uuid4()}.mp3"

            # Create and save the TextToSpeechAudio instance
            tts_audio_instance = TextToSpeechAudio(uploader=request.user)
            tts_audio_instance.audio_file.save(filename, audio_content)

            # Serialize and return the new instance
            serializer = self.get_serializer(tts_audio_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "AWS Polly did not return an audio stream."}, status=status.HTTP_400_BAD_REQUEST)


class AudioFileViewSet(mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class ImageFileViewSet(mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin, 
                       mixins.DestroyModelMixin, 
                       viewsets.GenericViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)