from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user_app.api.views import student_registration_view, LogoutAPIView, teacher_registration_view

urlpatterns = [
    path('student-register/', student_registration_view, name='register'),
    path('teacher-register/', teacher_registration_view, name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
]