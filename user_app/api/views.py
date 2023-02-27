from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from school.models import Student, Teacher

from rest_framework_simplejwt.tokens import RefreshToken
from user_app.api.serializers import RegistrationSerializer, LogoutSerializer



class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        print(request.data)

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', ])
def student_registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            Student.objects.create(email=data['email'], user_id_id=account.pk)


        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)




@api_view(['POST', ])
def teacher_registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            Teacher.objects.create(name=data['username'], user_id_id=account.pk)
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)