from .models import Teacher
from .models import Course
from .models import Student
from .models import StudentCourse
from .models import Semester
from .models import Assignment, TeacherAssignment
from django.contrib import admin

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(StudentCourse)
admin.site.register(Semester)
admin.site.register(Assignment)
admin.site.register(TeacherAssignment)