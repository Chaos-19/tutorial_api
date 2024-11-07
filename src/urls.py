from rest_framework.routers import DefaultRouter
from .views import TutorialViewSet, CategoryViewSet, CourseViewSet, SectionViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'tutorials', TutorialViewSet)
router.register(r'tutorials/(?P<tutorial_id>\d+)/categories', CategoryViewSet)
router.register(r'categories/(?P<category_id>\d+)/courses', CourseViewSet)
router.register(r'courses/(?P<course_id>\d+)/sections', SectionViewSet)
router.register(r'sections/(?P<section_id>\d+)/lessons', LessonViewSet)

urlpatterns = router.urls