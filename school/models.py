from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator

class Semester(models.Model):
    semester = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)])

    def __str__(self):
        return "semester " + str(self.semester)



class Teacher(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name



class Student(models.Model):
    class Status(models.TextChoices):
        approved = 'Approved', 'Approved'
        not_approved = 'Not Approved', 'Not Approved'

    class Gender(models.TextChoices):
        female = 'F', 'F'
        male = 'M', 'M'
        blank = '', ''

    stname = models.CharField(max_length=20)
    stsurname = models.CharField(max_length=20)
    email = models.CharField(max_length=180, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=25, null=True, blank=True)
    birthday = models.IntegerField(null=True, blank=True)
    gender = models.CharField(choices=Gender.choices, max_length=1, default=Gender.blank)
    approved = models.CharField(choices=Status.choices, max_length=20, default=Status.not_approved)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student')

    def __str__(self):
        return self.stname + " " + self.stsurname + "     | " + self.email



class Course(models.Model):

    class Status(models.TextChoices):
        available = 'Available', 'Available'
        not_available = 'Not Available', 'Not Available'

    coname = models.CharField(max_length=50)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student_id = models.ManyToManyField(Student, related_name='student', through='StudentCourse')
    semester_id = models.ForeignKey(Semester, related_name='semester2', on_delete=models.CASCADE, null=True, blank=True)
    course_start = models.DateField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.available)

    def __str__(self):
        return self.coname + " by " + str(self.teacher_id.name + " " +self.teacher_id.surname)


class StudentCourse(models.Model):

    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='StudentCourse')

    def __str__(self):
        return str(self.student_id) + " , " + str(self.course_id)

    class Meta:
        unique_together = ['course_id', 'student_id']


class TeacherAssignment(models.Model):
    assnum = models.IntegerField(default=0)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course4')
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['assnum', 'course_id']


class Assignment(models.Model):

    class Status(models.TextChoices):
        graded = 'Graded', 'Graded'
        not_graded = 'Not Graded', 'Not Graded'

    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='StudentCourse1')
    file = models.FileField(null=True, blank=True, upload_to='uploads/')
    teacher_assignment = models.ForeignKey(TeacherAssignment, on_delete=models.CASCADE, null=True, blank=True, related_name='assignment')
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.not_graded)

    def __str__(self):
        return "assignment "  + " for student " + str(self.student_id)

    @property
    def score_in_percentage(self):
        return f"{self.score}%"

    class Meta:
        unique_together = ['student_id', 'teacher_assignment']


class Waitlist(models.Model):

    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course2')
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='StudentCourse3')

    class Meta:
        unique_together = ['course_id', 'student_id']

