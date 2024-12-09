# courses/views.py
from rest_framework import viewsets
from .models import Course, Lecture, Material
from .serializers import CourseSerializer, LectureSerializer, MaterialSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrTeacher


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrTeacher]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
