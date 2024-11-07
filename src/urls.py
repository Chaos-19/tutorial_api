from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorialViewSet, CategoryViewSet, CourseViewSet, SectionViewSet, LessonViewSet

router = DefaultRouter()

# Registering the viewsets with the correct path converter format and basename
router.register(r'tutorials', TutorialViewSet, basename='tutorials')
router.register(r'tutorials/<int:tutorial_id>/categories', CategoryViewSet, basename='tutorial-categories')
router.register(r'categories/<int:category_id>/courses', CourseViewSet, basename='category-courses')
router.register(r'courses/<int:course_id>/sections', SectionViewSet, basename='course-sections')
router.register(r'sections/<int:section_id>/lessons', LessonViewSet, basename='section-lessons')

urlpatterns = [
    path('api/', include(router.urls)),  # This includes the router URLs
]
'''from rest_framework.routers import DefaultRouter
from src.views import TutorialViewSet, CategoryViewSet, CourseViewSet, SectionViewSet, LessonViewSet
from django.urls import path, include

router = DefaultRouter()

# Tutorials route
router.register(r'tutorials', TutorialViewSet, basename="tutorials")

# Categories route, with tutorial_id as a dynamic parameter
router.register(r'tutorials/(?P<tutorial_id>\d+)/categories', CategoryViewSet, basename="tutorial-categories")

# Courses route, with category_id as a dynamic parameter
router.register(r'categories/(?P<category_id>\d+)/courses', CourseViewSet, basename="category-courses")

# Sections route, with course_id as a dynamic parameter
router.register(r'courses/(?P<course_id>\d+)/sections', SectionViewSet, basename="course-sections")

# Lessons route, with section_id as a dynamic parameter
router.register(r'sections/(?P<section_id>\d+)/lessons', LessonViewSet, basename="section-lessons")

router.register(r'sections', SectionViewSet, basename="seections")

#urlpatterns = router.urls
urlpatterns = [
    path('api/', include(router.urls)),
]'''