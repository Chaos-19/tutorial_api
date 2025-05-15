from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Interview, Question
from .serializers import InterviewSerializer, QuestionSerializer

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    lookup_field = 'slug' 
    pagination_class = None  # Disable pagination

    @action(detail=True, methods=['get'])
    def questions(self, request, slug=None):
        interview = self.get_object()
        questions = interview.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search_by_title(self, request):
        title = request.query_params.get('title', None)
        if title:
            interviews = self.queryset.filter(title__icontains=title)
            serializer = self.get_serializer(interviews, many=True)
            return Response(serializer.data)
        return Response({'error': 'Title parameter is required'}, status=400)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = None  # Disable pagination

    @action(detail=False, methods=['get'])
    def search_by_text(self, request):
        text = request.query_params.get('text', None)
        if text:
            questions = self.queryset.filter(interview_question__icontains=text)
            serializer = self.get_serializer(questions, many=True)
            return Response(serializer.data)
        return Response({'error': 'Text parameter is required'}, status=400)