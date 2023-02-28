from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView
from school.admin_api.serializers import StudentUpdateSerializer, StudentDetailSerializer
from school.models import Student, Assignment, Course, StudentCourse
import pandas as pd
from user_app.api import permissions
from datetime import date
import datetime


def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

class StudentGroupByAge(APIView):
    permission_classes = (
        permissions.IsSuperUser,
    )

    def get(self, request):
        students = Student.objects.all()
        today = datetime.date.today()
        year = today.year
        age_distinct = students.values('birthday').distinct()
        age_final = [a['birthday'] for a in age_distinct]
        age_final_final = [year - a for a in age_final]
        list = []
        for age in sorted(age_final)[::-1]:
            name = Student.objects.filter(birthday = age).values_list('stname')
            list.append({'Age': year - age, 'name': name})
        return Response(list)


class StudentList(APIView):
    permission_classes = (
        permissions.IsSuperUser,
    )

    def get(self, request):
        students = Student.objects.all()
        list = []
        for student in students :
            list_students = {}
            score = Assignment.objects.filter(student_id=student).values_list('score')
            average = score.aggregate(Avg('score'))
            courses = StudentCourse.objects.filter(student_id=student).count()*3
            progress = round((score.count() / courses)*100,2)
            progres_final = f'{progress} % '
            list_students['name'] = student.stname
            if average['score__avg'] is None :
                list_students['average'] = 0
            else:
                list_students['average'] = int(average['score__avg'])
            list_students['progress'] = progres_final
            list.append(list_students)

        return Response(list)


class StudentListTop10(APIView):
    permission_classes = (
        permissions.IsSuperUser,
    )

    def get(self, request):
        students = Student.objects.all()
        list = []
        for student in students:
            list_students = {}
            score = Assignment.objects.filter(student_id=student).values_list('score')
            average = score.aggregate(Avg('score'))
            courses = StudentCourse.objects.filter(student_id=student).count() * 3
            progress = round((score.count() / courses) * 100, 2)
            progres_final = f'{progress} % '
            list_students['name'] = student.stname
            if average['score__avg'] is None:
                list_students['average'] = 0
            else:
                list_students['average'] = int(average['score__avg'])
            list_students['progress'] = progres_final
            list.append(list_students)
        newlist = sorted(list, key=lambda d: d['average'])[::-1][:2]
        return Response(newlist)



class StudentCourseTop100(APIView):
    permission_classes = (
        permissions.IsSuperUser,
    )

    def get(self, request):
        courses = Course.objects.all()
        print(courses)
        list = []
        for course in courses:
            list_course = {}
            score = Assignment.objects.filter(teacher_assignment__course_id = course).values_list('score')
            average = score.aggregate(Avg('score'))
            list_course['course name'] = course.coname
            if average['score__avg'] is not None :
                list_course['average'] = int(average['score__avg'])
                if list_course['average'] > 60 :
                    list.append(list_course)
            else:
                pass
        return Response(list)



class StudentGroupByCountry(APIView):
    permission_classes = (
        permissions.IsSuperUser,
    )

    def get(self, request):
        students = Student.objects.all()
        country_distinct = students.values('country').distinct()
        country_final = [a['country'] for a in country_distinct]
        print(country_final)
        list = []
        for country in country_final:
            name = Student.objects.filter(country = country).values_list('stname')
            list.append({'country': country, 'name': name})
        return Response(list)



class StudentGroupByGender(APIView):
    permission_classes = (
        permissions.IsSuperUser,
    )

    def get(self, request):
        students = Student.objects.all()
        gender_distinct = students.values('gender').distinct()
        gender_final = [a['gender'] for a in gender_distinct]
        list = []
        for gender in gender_final:
            name = Student.objects.filter(gender = gender).values_list('stname')
            list.append({'gender': gender, 'name': name})
        return Response(list)



class StudentUpdateList(APIView):
    permission_classes = (
        permissions.IsSuperUser,
    )
    def get(self, request):
        list = Student.objects.all()
        serializer = StudentDetailSerializer(list, many=True)
        return Response(serializer.data)


class StudentUpdate(APIView):
    def put(self, request, pk):
        student = Student.objects.get(id=pk)
        serializer = StudentUpdateSerializer(student, data={'id':student.id, 'approved': request.data['approved']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StudentNextYear(APIView):
    def get(self, request):
        new_student = pd.read_csv('/home/enkii/Desktop/new_students.csv')
        index = new_student[(new_student['first_name'].isnull()) | (new_student['country'] == 'Russia')].index
        new_student.drop(index, inplace=True)
        new_registration = new_student.to_dict(orient='records')
        return Response(new_registration)






