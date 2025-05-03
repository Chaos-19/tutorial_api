from rest_framework import serializers
from .models import QuizCourse, Quiz, Question, Option

class CloudinaryURLField(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.url
        return None

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "key", "text", "is_correct"]
        read_only_fields = ["id"]

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "detail", "output", "options"]
        read_only_fields = ["id"]

class QuizSerializer(serializers.ModelSerializer):
    #questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "title"]
        read_only_fields = ["id"]

class QuizCourseSerializer(serializers.ModelSerializer):
    icon = CloudinaryURLField()
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = QuizCourse
        fields = ["id", "title", "slug", "icon", "quizzes"]
        read_only_fields = ["id"]