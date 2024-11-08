from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tutorial, Category, Course, Section, Lesson
from .serializers import TutorialSerializer, CategorySerializer, CourseSerializer, SectionSerializer, LessonSerializer


class TutorialViewSet(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # List categories associated with a specific tutorial
    @action(detail=True, methods=['get'])
    def categories(self, request, pk=None):
        tutorial = self.get_object()
        categories = tutorial.categories.all()  # Related name in Category model
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    # Filter tutorials by title
    @action(detail=False, methods=['get'])
    def search_by_title(self, request):
        title = request.query_params.get('title', None)
        if title is not None:
            tutorials = self.queryset.filter(title__icontains=title)
            serializer = self.get_serializer(tutorials, many=True)
            return Response(serializer.data)
        return Response({"error": "Title parameter is required"}, status=400)
  
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    # List courses within a specific category
    @action(detail=True, methods=['get'])
    def courses(self, request, slug=None):
        category = self.get_object()
        courses = category.courses.all()  # Related name in Course model
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    
    # Filter categories by name
    @action(detail=False, methods=['get'])
    def search_by_name(self, request):
        name = request.query_params.get('name', None)
        if name:
            categories = self.queryset.filter(name__icontains=name)
            serializer = self.get_serializer(categories, many=True)
            return Response(serializer.data)
        return Response({"error": "Name parameter is required"}, status=400)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # List sections within a specific course
    @action(detail=True, methods=['get'])
    def sections(self, request, pk=None):
        course = self.get_object()
        sections = course.sections.all()  # Related name in Section model
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)
    
    # Filter courses by title
    @action(detail=False, methods=['get'])
    def search_by_title(self, request):
        title = request.query_params.get('title', None)
        if title:
            courses = self.queryset.filter(title__icontains=title)
            serializer = self.get_serializer(courses, many=True)
            return Response(serializer.data)
        return Response({"error": "Title parameter is required"}, status=400)

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # List lessons within a specific section
    @action(detail=True, methods=['get'])
    def lessons(self, request, slug=None):
        section = self.get_object()
        lessons = section.lesson_section.all()  # Related name in Lesson model
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    
    # Filter sections by title
    @action(detail=False, methods=['get'])
    def search_by_title(self, request):
        title = request.query_params.get('title', None)
        if title:
            sections = self.queryset.filter(title__icontains=title)
            serializer = self.get_serializer(sections, many=True)
            return Response(serializer.data)
        return Response({"error": "Title parameter is required"}, status=400)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Filter lessons by parent type and ID
    @action(detail=False, methods=['get'])
    def by_parent(self, request):
        content_type = request.query_params.get('content_type', None)
        object_id = request.query_params.get('object_id', None)
        if content_type and object_id:
            try:
                content_type_obj = ContentType.objects.get(model=content_type)
                lessons = self.queryset.filter(content_type=content_type_obj, object_id=object_id)
                serializer = self.get_serializer(lessons, many=True)
                return Response(serializer.data)
            except ContentType.DoesNotExist:
                return Response({"error": "Invalid content type"}, status=400)
        return Response({"error": "content_type and object_id parameters are required"}, status=400)
    
    # Search lessons by title
    @action(detail=False, methods=['get'])
    def search_by_title(self, request):
        title = request.query_params.get('title', None)
        if title:
            lessons = self.queryset.filter(title__icontains=title)
            serializer = self.get_serializer(lessons, many=True)
            return Response(serializer.data)
        return Response({"error": "Title parameter is required"}, status=400)