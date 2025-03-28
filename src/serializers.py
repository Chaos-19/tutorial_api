from rest_framework import serializers
from .models import Tutorial, Category, Course, Section, Lesson
from django.contrib.contenttypes.models import ContentType

class CloudinaryURLField(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.url
        return None

class TutorialSerializer(serializers.ModelSerializer):
    img = CloudinaryURLField()
    
    class Meta:
        model = Tutorial
        fields = ["id","img", "title"]
        read_only_fields = ['id']  

class CourseSerializer(serializers.ModelSerializer):
    #category = CategorySerializer()  # Nested representation of Category
    icon = CloudinaryURLField()

    class Meta:
        model = Course
        fields = ["id",'title', 'icon', 'description','is_nested']
        read_only_fields = ['id']  

class CategorySerializer(serializers.ModelSerializer):
    #tutorial = TutorialSerializer()  # Nested representation of Tutorial
    courses = CourseSerializer(many=True, read_only=True)
    icon = CloudinaryURLField()

    class Meta:
        model = Category
        fields = ["id",'name', 'icon', 'slug','courses']
        read_only_fields = ['id']  


class SectionSerializer(serializers.ModelSerializer):
    #course = CourseSerializer()  # Nested representation of Course
    icon = CloudinaryURLField()

    class Meta:
        model = Section
        fields = ['title', 'icon', 'slug', 'description', 'course']


class LessonSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(source='content_type.name', read_only=True)  # Readable content type name
    #parent_detail = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['title', 'content', 'object_id', 'content_type', 'content_type_name']

    def get_parent_detail(self, obj):
        """Dynamically serialize the parent based on content type"""
        if obj.content_type.model == 'section':
            return SectionSerializer(obj.parent).data
        elif obj.content_type.model == 'course':
            return CourseSerializer(obj.parent).data
        return None