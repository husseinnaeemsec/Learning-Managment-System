from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lecture, Material
from .serializers import CourseSerializer, LectureSerializer, MaterialSerializer
from .permissions import IsAdminOrTeacher

class CourseListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get_permissions(self):
        if self.request.method == "POST":
            # Restrict POST requests to authenticated users who are teachers
            return [IsAuthenticated(),IsAdminOrTeacher()]
        else:
            # Allow all authenticated users for GET
            return [IsAuthenticated()]


    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            response = {
                "course":serializer.data,
                "message":"Course Created",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LectureListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        lectures = Lecture.objects.filter(course_id=course_id)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not hasattr(request.user, 'role') or request.user.role != 'teacher':
            return Response({"error": "Only teachers can create courses."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MaterialListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, lecture_id):
        materials = Material.objects.filter(lecture_id=lecture_id)
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request, lecture_id):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(lecture_id=lecture_id)
            return Response(serializer, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
