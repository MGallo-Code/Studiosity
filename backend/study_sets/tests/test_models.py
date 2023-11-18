from django.test import TestCase
from study_sets.models import StudySet, Tag

class StudySetModelTest(TestCase):
    def setUp(self):
        self.study_set = StudySet.objects.create(
            title="Test Study Set",
            description="Test Description"
        )

    def test_study_set_creation(self):
        self.assertEqual(self.study_set.title, "Test Study Set")
        self.assertEqual(self.study_set.description, "Test Description")

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="TeSttag")
    
    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "testtag")