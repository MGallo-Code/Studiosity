from math import ceil

from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.pagination import PageNumberPagination

from .models import StudySet, StudyTerm, Tag
from .serializers import StudySetSerializer, StudyTermSerializer, TagSerializer


class CustomPagination(PageNumberPagination):
    page_size = 25

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
        return obj.uploader == request.user or request.user.is_superuser

class IsOwnerOfRelatedStudySet(BasePermission):
    """Allow access if the user is the owner of the related study set."""
    def has_object_permission(self, request, view, obj):
        return obj.study_set.uploader == request.user

class CanViewStudyTerm(BasePermission):
    """
    Allow access to view a study term if the user is an admin, the owner of the related study set,
    or if the related study set is not private.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        if view.action == 'retrieve':
            study_term_id = view.kwargs.get('pk')
            study_term = get_object_or_404(StudyTerm, pk=study_term_id)
            return study_term.study_set.uploader == user or not study_term.study_set.private
        return True

class MyStudySetsView(generics.ListAPIView):
    serializer_class = StudySetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        This view should return a list of all the study sets
        for the currently authenticated user.
        """
        user = self.request.user
        return StudySet.objects.filter(uploader=user)

class PublicStudySetsView(generics.ListAPIView):
    serializer_class = StudySetSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        This view returns a list of all the public study sets.
        """
        return StudySet.objects.filter(private=False)
    
class AllStudySetsView(generics.ListAPIView):
    serializer_class = StudySetSerializer
    permission_classes = [IsSuperuser]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        This view returns a list of all the study sets.
        Admin privilege required.
        """
        return StudySet.objects.all()

class StudySetViewSet(viewsets.GenericViewSet, 
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    """
    A viewset that provides `retrieve`, `update`, and `delete` actions
    on study sets.
    """
    serializer_class = StudySetSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsOwnerOrSuperuser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Returns a queryset of study sets based on the user's permission.
        """
        user = self.request.user
        if user.is_superuser:
            return StudySet.objects.all()
        
        return StudySet.objects.filter(uploader=user) | StudySet.objects.filter(private=False)

class CreateStudySetView(generics.CreateAPIView):
    """
    API endpoint for creating a new study set.
    Requires the user to be authenticated.
    """
    serializer_class = StudySetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Sets the uploader to the current user upon creation.
        """
        serializer.save(uploader=self.request.user)

class StudyTermsInSetView(generics.ListAPIView):
    serializer_class = StudyTermSerializer

    def get_queryset(self):
        """
        This view returns a list of study terms for a specific study set.
        """
        study_set_id = self.kwargs['pk']
        study_set = get_object_or_404(StudySet, id=study_set_id)

        if study_set.private and not (study_set.uploader == self.request.user or self.request.user.is_superuser):
            raise PermissionDenied(detail="You do not have permission to view these study terms.")
        
        return StudyTerm.objects.filter(study_set=study_set)

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

        serializer.save(study_set=study_set)
    
    def perform_update(self, serializer):
        """
        Override perform_update to check the uploader of the image and audio files.
        """
        user = self.request.user
        data = serializer.validated_data

        for field in ['front_image', 'back_image', 'front_audio', 'back_audio']:
            file_object = data.get(field)
            if file_object and file_object.uploader != user:
                raise PermissionDenied(detail=f"You do not have permission to use this {field.split('_')[0]}.")

        serializer.save()

class TagViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, and deleting tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """
        Only authenticated users can create or delete tags.
        """
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
