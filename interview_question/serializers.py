from rest_framework import serializers
from .models import Interview, Question
from src.models import Tutorial

class CloudinaryURLField(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.url
        return None

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'interview_question', 'answer']
        read_only_fields = ['id']

class InterviewSerializer(serializers.ModelSerializer):
    icon = CloudinaryURLField()
    """
    questions = QuestionSerializer(many=True, read_only=True)
    tutorial_id = serializers.PrimaryKeyRelatedField(
        queryset=Tutorial.objects.all(), source='tutorial', required=True
    )"""

    class Meta:
        model = Interview
        fields = ['id', 'title', 'slug', 'icon']
        #read_only_fields = ['id']