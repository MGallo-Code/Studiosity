from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from .models import StudySet, StudyTerm, Tag
from .serializers import StudySetSerializer, StudyTermSerializer, TagSerializer


class IsSuperuser(BasePermission):
    """
    Custom permission to only allow superusers to access it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

class IsOwnerOrSuperuser(BasePermission):
    """
    Custom permission to only allow owners of an object or superusers to access it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.uploader == request.user or request.user.is_superuser

class IsOwnerOfRelatedStudySetOrSuperuser(BasePermission):
    """
    Custom permission to only allow owners of the related study set or superusers to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Assuming the related study set is accessible via 'study_set' attribute
        return obj.study_set.uploader == request.user or request.user.is_superuser

class MyStudySetsView(generics.ListAPIView):
    serializer_class = StudySetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the study sets
        for the currently authenticated user.
        """
        user = self.request.user
        return StudySet.objects.filter(uploader=user)

class PublicStudySetsView(generics.ListAPIView):
    serializer_class = StudySetSerializer

    def get_queryset(self):
        """
        This view returns a list of all the public study sets.
        """
        return StudySet.objects.filter(private=False)
    
class AllStudySetsView(generics.ListAPIView):
    serializer_class = StudySetSerializer
    permission_classes = [IsSuperuser]

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
        Returns a study set based on the user's permission.
        """
        user = self.request.user
        if user.is_superuser:
            return StudySet.objects.all()

        return StudySet.objects.filter(id=self.kwargs['pk'], uploader=user) | StudySet.objects.filter(id=self.kwargs['pk'], private=False)

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
