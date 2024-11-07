from rest_framework import serializers
from .models import Tutorial,Category,Course,Section,Lesson


class TutorialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tutorial
        fields = '__all__' # ["img","title"]

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' # ['name', 'icon','slug', 'tutorial']
        
class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = '__all__' # ['title', 'icon','description', 'category']
        
class SectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Section
        fields = '__all__' # ['title', 'icon','slug','description', 'course']
        
class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__' # ['title', 'content','object_id', 'content_type','parent']
