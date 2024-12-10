from django.urls import path
from .views import CourseListCreateView, LectureListCreateView, MaterialListCreateView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:course_id>/lectures/', LectureListCreateView.as_view(), name='lecture-list-create'),
    path('lectures/<int:lecture_id>/materials/', MaterialListCreateView.as_view(), name='material-list-create'),
]
