from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quiz, Question, Option
from .serializers import QuizSerializer, QuestionSerializer, OptionSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = "slug"  # Use slug for lookups instead of pk

    @action(detail=True, methods=["get"])
    def questions(self, request, slug=None):
        quiz = self.get_object()
        questions = quiz.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search_by_title(self, request):
        title = request.query_params.get("title", None)
        if title:
            quizzes = self.queryset.filter(title__icontains=title)
            serializer = self.get_serializer(quizzes, many=True)
            return Response(serializer.data)
        return Response({"error": "Title parameter is required"}, status=400)

    @action(detail=False, methods=["get"])
    def by_tutorial(self, request):
        tutorial_id = request.query_params.get("tutorial_id", None)
        if tutorial_id:
            quizzes = self.queryset.filter(tutorial__id=tutorial_id)
            serializer = self.get_serializer(quizzes, many=True)
            return Response(serializer.data)
        return Response({"error": "Tutorial ID parameter is required"}, status=400)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=True, methods=["get"])
    def options(self, request, pk=None):
        question = self.get_object()
        options = question.options.all()
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search_by_text(self, request):
        text = request.query_params.get("text", None)
        if text:
            questions = self.queryset.filter(text__icontains=text)
            serializer = self.get_serializer(questions, many=True)
            return Response(serializer.data)
        return Response({"error": "Text parameter is required"}, status=400)

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    @action(detail=False, methods=["get"])
    def search_by_text(self, request):
        text = request.query_params.get("text", None)
        if text:
            options = self.queryset.filter(text__icontains=text)
            serializer = self.get_serializer(options, many=True)
            return Response(serializer.data)
        return Response({"error": "Text parameter is required"}, status=400)