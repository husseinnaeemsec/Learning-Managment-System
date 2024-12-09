# courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LectureViewSet, MaterialViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('lectures', LectureViewSet)
router.register('materials', MaterialViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
