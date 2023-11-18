from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from study_sets.models import StudySet, StudyTerm
from study_sets.serializers import StudySetSerializer, StudyTermSerializer

class StudySetViewTestCase(APITestCase):

    def setUp(self):
        self.study_set1 = StudySet.objects.create(title="Set 1", description="Description 1")
        self.study_set2 = StudySet.objects.create(title="Set 2", description="Description 2")
        self.study_term1 = StudyTerm.objects.create(study_set=self.study_set1, front_text="Front 1", back_text="Back 1")
        self.study_term2 = StudyTerm.objects.create(study_set=self.study_set1, front_text="Front 2", back_text="Back 2")

    def test_get_study_sets(self):
        # Testing retrieval of all study sets
        url = reverse('studyset-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_study_set(self):
        # Testing retrieval of a single study set
        url = reverse('studyset-detail', args=[self.study_set1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, StudySetSerializer(self.study_set1).data)

    def test_get_study_set_terms(self):
        # Testing the custom 'terms' action
        url = reverse('studyset-terms', args=[self.study_set1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, StudyTermSerializer([self.study_term1, self.study_term2], many=True).data)
