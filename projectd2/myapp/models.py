from django.db import models
from django.contrib.auth.models import AbstractUser


# Department Model
class Department(models.Model):
    department = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.department


class User(AbstractUser):
    USERTYPE_CHOICES = (
        ("Student", "Student"),
        ("Teacher", "Teacher"),
    )

    usertype = models.CharField(max_length=50, choices=USERTYPE_CHOICES)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    picture = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.usertype})"


class Teacher(models.Model):
    teacher_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)  

    def __str__(self):
        return f"Teacher: {self.teacher_id.username}"


# Student Model
class Student(models.Model):
    student_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    guardian = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Student: {self.student_id.username}"
        



class Notes(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="notes/")   
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
