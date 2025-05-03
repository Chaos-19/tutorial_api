from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import QuizCourseViewSet, QuizViewSet, QuestionViewSet, OptionViewSet

router = DefaultRouter()
router.register(r"quiz-courses", QuizCourseViewSet, basename="quizcourse")
router.register(r"quizzes", QuizViewSet, basename="quiz")
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"options", OptionViewSet, basename="option")

urlpatterns = [
    path("", include(router.urls)),
]