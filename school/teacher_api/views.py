from rest_framework.response import Response
from rest_framework import permissions as perm
from user_app.api.permissions import IsStaffUser
from rest_framework.views import APIView
from school.models import TeacherAssignment, Assignment, Course, Student, Teacher
from school.teacher_api.serializers import TeacherAssignmentSerializer, AssignmentGradeSerializer
from school.student_api.views import get_progress


class TeacherAssignmentPost(APIView):
    permission_classes = (
        perm.IsAuthenticated,
        IsStaffUser
    )

    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user_id=request.user)
        list = TeacherAssignment.objects.filter(teacher_id=teacher.id)
        serializer = TeacherAssignmentSerializer(list, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user_id=request.user)
        serializer = TeacherAssignmentSerializer(data= {'assnum':request.data['assnum'], 'course_id': request.data['course_id'], 'teacher_id': teacher.id})
        assignments = TeacherAssignment.objects.filter(course_id=request.data['course_id']).count()
        if serializer.is_valid():
            courses = Course.objects.filter(teacher_id=teacher.id).values('id')
            course_list = [course['id'] for course in courses]
            if request.data['course_id'] not in course_list:
                return Response({"MSG" : "You are not teaching on this course"})
            if assignments > 2:
                return Response({"MSG": "Not more than 3 assignments"})
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TeacherAssignmentGrade(APIView):
    permission_classes = (
        perm.IsAuthenticated,
        IsStaffUser
    )

    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user_id=request.user)
        list = Assignment.objects.filter(teacher_assignment__teacher_id=teacher.id)
        serializer = AssignmentGradeSerializer(list, many=True)
        return Response(serializer.data)


class TeacherAssignmentGradeSpecific(APIView):
    permission_classes = (
        perm.IsAuthenticated,
        IsStaffUser
        )

    def put(self, request, pk, **kwargs):
        teacher = Teacher.objects.get(user_id=request.user)
        list = Assignment.objects.get(id=pk)
        serializer = AssignmentGradeSerializer(list, data=request.data)
        if serializer.is_valid():
            if list.teacher_assignment.teacher_id_id == teacher.id :
                pass
            else:
                return Response({"MSG": "This student doesn't belong to your class"})
            serializer.save()
            Assignment.objects.filter(pk=request.data['id']).update(status='Graded')
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TeacherCourseList(APIView):
    permission_classes = (
        perm.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user_id=request.user)
        courses = Course.objects.filter(teacher_id=teacher.id)
        course_student = {}

        for course in courses:
            list_students = []
            students = Student.objects.filter(student=course.pk)
            for student in students:
                student_evaluation = Assignment.objects.filter(student_id=student,teacher_assignment__course_id=course.id).values_list()
                number_courses = student_evaluation.count()
                list_students.append({f'{student.stname}': [{st_ev[2]: st_ev[4] for st_ev in student_evaluation}, {'progress':get_progress(number_courses)}]})
            course_student[course.coname] = list_students

        return Response(course_student)
