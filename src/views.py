from rest_framework import viewsets
from .models import Tutorial, Category, Course, Section, Lesson
from .serializers import (
    TutorialSerializer, CategorySerializer, CourseSerializer,
    SectionSerializer, LessonSerializer
)

class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(tutorial_id=self.kwargs["tutorial_id"])

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(category_id=self.kwargs["category_id"])

class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer

    def get_queryset(self):
        # Fetch the sections related to a particular course
        return Section.objects.filter(course_id=self.kwargs["course_id"])

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        # Fetch the lessons related to a particular section
        return Lesson.objects.filter(section_id=self.kwargs["section_id"])