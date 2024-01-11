from math import ceil
import uuid
from boto3 import Session, client

from django.db.models import Max, Q
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from uploads.models import ImageFile, TextToSpeechAudio
from .models import StudySet, StudyTerm, Tag, Favorite
from .serializers import StudySetSerializer, StudyTermSerializer, PublicSetsDetailSerializer, TagSerializer


class CustomPagination(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        current_page = self.request.query_params.get(self.page_query_param, 1)
        total_pages = ceil(self.page.paginator.count / self.page_size)

        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'total_pages': total_pages,
            'current_page': int(current_page),
            'results': data
        })

class IsSuperuser(BasePermission):
    """
    Custom permission to only allow superusers to access it.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsOwnerOrSuperuser(BasePermission):
    """
    Custom permission to only allow owners of an object or superusers to access it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user and (obj.uploader == request.user or request.user.is_superuser)


class IsOwnerOfRelatedStudySet(BasePermission):
    """Allow access if the user is the owner of the related study set."""
    def has_object_permission(self, request, view, obj):
        return request.user and obj.study_set.uploader == request.user


class CanViewStudyTerm(BasePermission):
    """
    Allow access to view a study term if the user is an admin, the owner of the related study set,
    or if the related study set is not private.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True

        if hasattr(view, 'action'):
            # ViewSet specific logic (if you're dealing with a ViewSet)
            if view.action == 'retrieve':
                return self._check_study_term_permission(view.kwargs.get('pk'), user)
        else:
            # Generic APIView or generics.ListAPIView specific logic
            return self._check_study_terms_in_set_permission(view.kwargs.get('pk'), user)

        return False

    def _check_study_term_permission(self, study_term_id, user):
        try:
            study_term = StudyTerm.objects.get(pk=study_term_id)
            return study_term.study_set.uploader == user or not study_term.study_set.private
        except StudyTerm.DoesNotExist:
            raise PermissionDenied(detail="No such study term exists or you do not have permission to view it.")

    def _check_study_terms_in_set_permission(self, study_set_id, user):
        try:
            study_set = StudySet.objects.get(id=study_set_id)
            return study_set.uploader == user or not study_set.private
        except StudySet.DoesNotExist:
            raise PermissionDenied(detail="No such study set exists or you do not have permission to view it.")

class MySetsView(generics.ListAPIView):
    serializer_class = StudySetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        This view should return a list of all the study sets
        owned by the currently authenticated user.
        """
        user = self.request.user
        return StudySet.objects.filter(uploader=user)

class PublicSetsView(generics.ListAPIView):
    """
    Returns all public study sets for any user
    """
    serializer_class = StudySetSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return StudySet.objects.filter(private=False)

class PublicSetDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single public study set along with its terms.
    """
    serializer_class = PublicSetsDetailSerializer
    queryset = StudySet.objects.filter(private=False)

    def get_object(self):
        """
        Override the standard get_object method to ensure that only public study sets can be retrieved.
        """
        pk = self.kwargs.get('pk')
        try:
            return StudySet.objects.get(pk=pk, private=False)
        except StudySet.DoesNotExist:
            raise NotFound('A public study set with this ID does not exist.')

class StudySetViewSet(viewsets.ModelViewSet):
    """
    Returns all study sets for superusers.
    Returns sets owned by the user for authenticated non-superusers.
    """
    serializer_class = StudySetSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return StudySet.objects.all()
            else:
                return StudySet.objects.filter(Q(uploader=user))
        else:
            return StudySet.objects.filter(Q(private=False))

    def get_permissions(self):
        """
        Custom permissions based on action.
        """
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated()]
        else:  # update, partial_update, destroy
            return [IsOwnerOrSuperuser()]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class StudyTermsInSetView(generics.ListAPIView):
    serializer_class = StudyTermSerializer
    permission_classes = [CanViewStudyTerm]

    def get_queryset(self):
        study_set_id = self.kwargs['pk']
        study_set = get_object_or_404(StudySet, id=study_set_id)

        if study_set.private and not (self.request.user.is_authenticated and (study_set.uploader == self.request.user or self.request.user.is_superuser)):
            raise PermissionDenied(detail="You do not have permission to view these study terms.")
        
        return StudyTerm.objects.filter(study_set=study_set)


class UpdateSortOrderView(APIView):
    def post(self, request, *args, **kwargs):
        study_set_id = kwargs.get('study_set_id')
        term_order = request.data.get('term_order')

        if not term_order:
            return Response({"error": "No term order provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Assign intermediate values
        for index, term_id in enumerate(term_order):
            intermediate_sort_order = index + len(term_order)  # Ensure the intermediate value is outside the current range
            StudyTerm.objects.filter(id=term_id, study_set_id=study_set_id).update(sort_order=intermediate_sort_order)

        # Step 2: Assign final values
        for index, term_id in enumerate(term_order):
            StudyTerm.objects.filter(id=term_id, study_set_id=study_set_id).update(sort_order=index)

        return Response({"message": "Sort order updated successfully"}, status=status.HTTP_200_OK)


class StudyTermViewSet(viewsets.ModelViewSet):
    serializer_class = StudyTermSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create']:
            return [IsAuthenticated(), IsOwnerOfRelatedStudySet()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOfRelatedStudySet()]
        elif self.action in ['retrieve']:
            return [CanViewStudyTerm()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Returns a queryset of study terms based on the user's permission.
        """
        if self.request.user.is_superuser:
            return StudyTerm.objects.all()
        return StudyTerm.objects.filter(study_set__uploader=self.request.user) | StudyTerm.objects.filter(study_set__private=False)

    def perform_create(self, serializer):
        """
        Sets the study set to one owned by the user upon creation.
        """
        user = self.request.user
        study_set_id = self.request.data.get('study_set')

        try:
            study_set = StudySet.objects.get(pk=study_set_id)
        except StudySet.DoesNotExist:
            raise PermissionDenied(detail="Study set not found.")

        if study_set.uploader != user:
            raise PermissionDenied(detail="You do not have permission to add terms to this study set.")

        last_sort_order = StudyTerm.objects.aggregate(Max('sort_order'))['sort_order__max'] or 0

        instance = serializer.save(study_set=study_set, sort_order=last_sort_order + 1)
        instance = self.handle_tts_update(instance)
        instance.save()
    
    def perform_update(self, serializer):
        user = self.request.user
        data = serializer.validated_data

        instance = self.get_object()

        # If images or audio are being updated, delete previous images/audio
        for field in ['front_image', 'back_image', 'front_audio', 'back_audio']:
            file_object = data.get(field)

            # Check if a new file is being set and if the user has permission
            if file_object and file_object.uploader != user:
                raise PermissionDenied(detail=f"You do not have permission to use this {field.split('_')[1]}.")

            # Check and delete the old file if necessary
            old_file = getattr(instance, field)
            if file_object and old_file and old_file.id != file_object.id:
                old_file.delete()
            
        # Note fields where text is changing or new voice_id selected
        changed_fields = []
        for field in ['front_text', 'back_text', 'front_voice_id', 'back_voice_id']:
            field_value = data.get(field)
            if getattr(instance, field) and field_value != getattr(instance, field):
                changed_fields.append(field)
        
        # Update study_term
        instance = serializer.save()

        # If text changed or new voice_id selected, delete old TTS audio
        for field in changed_fields:
            # Get 'front' or 'back' to decide which tts to delete
            side = field.split('_')[0]
            # delete old tts audio
            old_file = getattr(instance, side + '_tts_audio')
            if old_file:
                old_file.delete()
                setattr(instance, side + '_tts_audio', None)
            
        # Generate new tts edits if necessary
        instance = self.handle_tts_update(instance)
        # Save tts edits
        instance.save()
    
    def handle_tts_update(self, instance):
        # If missing front TTS audio
        if not instance.front_tts_audio:
            instance = self.generate_tts_audio('front', instance)
            
        # If missing back TTS audio
        if not instance.back_tts_audio:
            instance = self.generate_tts_audio('back', instance)
        
        return instance

    def generate_tts_audio(self, side, instance):
        text = getattr(instance, side + '_text')
        voice_id = getattr(instance, side + '_voice_id')

        # Generate new TTS audio if text has changed
        if text and text.strip() != '':
            # Initialize AWS Polly client
            polly = Session(region_name='us-east-2').client('polly')

            # Generate TTS audio
            response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId=voice_id)
            if "AudioStream" in response:
                audio_content = ContentFile(response['AudioStream'].read())
                filename = f"{uuid.uuid4()}.mp3"

                # Create a new TextToSpeechAudio instance
                tts_audio_instance = TextToSpeechAudio(uploader=self.request.user)
                tts_audio_instance.file.save(filename, audio_content)

                tts_audio_instance.save()

                # Set the new TTS instance to the study term
                setattr(instance, side + '_tts_audio', tts_audio_instance)
        
        return instance


class PollyVoicesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Initialize AWS Polly client
        polly_client = client('polly', region_name='us-east-1')

        try:
            # Fetch the available voices
            response = polly_client.describe_voices()
            
            # Extract the voice data
            voices = response.get('Voices', [])
            
            # Return the list of voices
            return Response({'voices': voices}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle exceptions
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FavoriteStudySetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        study_set = get_object_or_404(StudySet, pk=pk)
        user = request.user
        favorite, created = Favorite.objects.get_or_create(user=user, study_set=study_set)

        if not created:
            favorite.delete()
            return Response({'status': 'unfavorited'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'status': 'favorited'}, status=status.HTTP_201_CREATED)