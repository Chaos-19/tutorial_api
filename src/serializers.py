from rest_framework import serializers
from .models import Tutorial, Category, Course, Section, Lesson
from django.contrib.contenttypes.models import ContentType


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ["img", "title", "created_at", "updated_at"]


class CategorySerializer(serializers.ModelSerializer):
    tutorial = TutorialSerializer()  # Nested representation of Tutorial

    class Meta:
        model = Category
        fields = ['name', 'icon', 'slug', 'tutorial', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested representation of Category

    class Meta:
        model = Course
        fields = ['title', 'icon', 'description', 'category', 'created_at', 'updated_at']


class SectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Nested representation of Course

    class Meta:
        model = Section
        fields = ['title', 'icon', 'slug', 'description', 'course', 'created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(source='content_type.name', read_only=True)  # Readable content type name
    parent_detail = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['title', 'content', 'object_id', 'content_type', 'content_type_name', 'parent_detail', 'created_at', 'updated_at']

    def get_parent_detail(self, obj):
        """Dynamically serialize the parent based on content type"""
        if obj.content_type.model == 'section':
            return SectionSerializer(obj.parent).data
        elif obj.content_type.model == 'course':
            return CourseSerializer(obj.parent).data
        return None