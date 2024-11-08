from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TutorialViewSet, CategoryViewSet, CourseViewSet, SectionViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'tutorials', TutorialViewSet, basename='tutorial')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
]