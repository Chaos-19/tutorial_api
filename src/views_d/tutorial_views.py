'''
from src.models import Tutorial
from src.serializers import TutorialSerializer
from rest_framework import permissions,renderers,viewsets
'''
from .models import Tutorial, Category, Course, Section, Lesson
from .serializers import (
    TutorialSerializer, CategorySerializer, CourseSerializer,
    SectionSerializer, LessonSerializer
)

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

@csrf_exempt
def tutorial_list(request):
    if request.method == "GET":
      
        tutorial = Tutorial.objects.all()
        serializer = TutorialSerializer(tutorial,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.methid == "POST":
        data = JSONParser().parse(request)
        serializer = TutorialSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors, status=400)   
    
  