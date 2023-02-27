from django.urls import path
from school.admin_api.views import StudentList, StudentUpdate, StudentListTop10, StudentNextYear, StudentUpdateList, StudentCourseTop100, StudentGroupByCountry, StudentGroupByGender, StudentGroupByAge


urlpatterns = [
    path('student-list/', StudentList.as_view(), name='student-detail'),
    path('student-top-2/', StudentListTop10.as_view(), name='student-detail'),
    path('course-top/', StudentCourseTop100.as_view(), name='student-detail'),
    path('student-update/', StudentUpdateList.as_view(), name='student-detail'),
    path('group-by-country/', StudentGroupByCountry.as_view(), name='student-next-year'),
    path('group-by-age/', StudentGroupByAge.as_view(), name='student-next-year'),
    path('group-by-gender/', StudentGroupByGender.as_view(), name='student-next-year'),
    path('student-update/<int:pk>/', StudentUpdate.as_view(), name='student-detail'),
    path('student-next-year/', StudentNextYear.as_view(), name='student-next-year'),
    ]