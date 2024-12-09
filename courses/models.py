# courses/models.py
from django.db import models
from users.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, related_name='courses', limit_choices_to={'role': 'student'})

    def __str__(self):
        return self.title

class Lecture(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    content = models.TextField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Material(models.Model):
    MATERIAL_TYPES = [
        ('video', 'Video'),
        ('note', 'Note'),
        ('digital', 'Digital Material'),
    ]
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='materials')
    type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(upload_to='materials/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.lecture.title}"
