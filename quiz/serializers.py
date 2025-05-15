from rest_framework import serializers
from .models import Quiz, Question, Option

class CloudinaryURLField(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.url
        return None


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'key', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'detail', 'output', 'options']

class QuizSerializer(serializers.ModelSerializer):
    #questions = QuestionSerializer(many=True, read_only=True)
    icon = CloudinaryURLField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'slug', 'icon']