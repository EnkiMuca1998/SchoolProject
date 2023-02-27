from django.urls import path
from school.student_api.views import CourseRegistration, AssignmentList, StudentDetail, StudentPersonalDetails, CourseList


urlpatterns = [

    path('personal-details/', StudentPersonalDetails.as_view(), name='student-personal-detail'),
    path('academic-details/', StudentDetail.as_view(), name='student-academic-detail'),
    path('course-list/semester/<int:pk>/', CourseList.as_view(), name='course-list'),
    path('course-register/', CourseRegistration.as_view(), name='course-registration'),
    path('assignment-submit/', AssignmentList.as_view(), name='assignment-list / submission'),
    ]