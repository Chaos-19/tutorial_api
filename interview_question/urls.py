from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import InterviewViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'interviews', InterviewViewSet, basename='interview')
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
]