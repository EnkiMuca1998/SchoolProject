from django.urls import path
from school.teacher_api.views import TeacherAssignmentPost, TeacherAssignmentGrade, TeacherCourseList, TeacherAssignmentGradeSpecific

urlpatterns = [
    path('submit-assignment/', TeacherAssignmentPost.as_view(), name='student-detail'),
    path('grade/', TeacherAssignmentGrade.as_view(), name='student-detail'),
    path('grade/<int:pk>/', TeacherAssignmentGradeSpecific.as_view(), name='student-detail'),
    path('course-list/', TeacherCourseList.as_view(), name='student-detail'),
    ]