from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from src.models import Tutorial
from src.serializers import TutorialSerializer
from rest_framework import permissions,renderers,viewsets

class TutorialListView(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = []
    
    
  