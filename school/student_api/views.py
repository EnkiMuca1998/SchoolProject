from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from school.student_api.serializers import AddStudentSerializer, CourseListSerializer, CourseRegistrationSerializer, WaitlistSerializer, AssignmentSubmissionSerializer, AssignmentListSerializer, StudentDetailSerializer
from school.models import Student, Course, StudentCourse, TeacherAssignment, Assignment


def get_progress(num):
    if num == 1:
        return "33%"
    if num == 2:
        return "66%"
    if num == 3:
        return "100%"
    return "0%"


class StudentDetail(APIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user_id=request.user)
        assignments = Assignment.objects.filter(student_id=student.id)
        codistinct = assignments.values('teacher_assignment__course_id').distinct()
        course = [a['teacher_assignment__course_id'] for a in codistinct]
        final_values = []

        for i in course:
            list_grades = [a[0] for a in assignments.filter(teacher_assignment__course_id_id=i).values_list('score')]
            #course[i-1]
            final_values.append({'course':Course.objects.get(pk=i).coname, 'notat': list_grades, 'average': sum(list_grades)/len(list_grades), 'progress': get_progress(len(list_grades))})
            print(sum(list_grades))

        serializer = StudentDetailSerializer(final_values, many=True)
        self.check_object_permissions(request, final_values)
        return Response(serializer.data)



class StudentPersonalDetails(APIView):

    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user_id=request.user)
        details = Student.objects.get(pk = student.id)
        serializer = AddStudentSerializer(details)
        return Response(serializer.data)


    def put(self, request, *args, **kwargs):
        student = Student.objects.get(user_id=request.user)
        list = Student.objects.get(id = student.id)
        serializer = AddStudentSerializer(list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CourseList(APIView):

    def get(self, request, pk):
        list = Course.objects.filter(semester_id=pk)
        serializer = CourseListSerializer(list, many=True)
        return Response(serializer.data)


class CourseRegistration(APIView):

        # permission_classes = (
        #     permissions.IsAuthenticated,
        # )

        def post(self, request, *args, **kwargs):
            student = Student.objects.get(user_id=request.user)
            reg_student = StudentCourse.objects.filter(student_id=student.id).count()
            reg_courses = StudentCourse.objects.filter(course_id=request.data['course_id']).count()
            serializer = CourseRegistrationSerializer(data={'student_id': student.id, 'course_id': request.data['course_id']})
            if serializer.is_valid():
                if reg_student >= 3:
                    return Response({"MSG": "You cannot register in more than 3 courses"})
                if reg_courses >= 5:
                    Course.objects.filter(pk=request.data['course_id']).update(status='Not Available')
                    waitlist_serializer = WaitlistSerializer(data={'student_id': student.id, 'course_id': request.data['course_id']})
                    if waitlist_serializer.is_valid():
                        waitlist_serializer.save()
                        return Response({"MSG":"You have been added to the waitlist"})
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)


class AssignmentList(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user_id=request.user)
        list = TeacherAssignment.objects.filter(course_id__course__student_id=student.id).exclude(assignment__student_id=student.id)
        serializer = AssignmentListSerializer(list, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        student = Student.objects.get(user_id=request.user)
        serializer = AssignmentSubmissionSerializer(data={'file': request.data['file'], 'student_id':student.id, 'teacher_assignment': request.data['teacher_assignment']})
        teacher_assignment_list = TeacherAssignment.objects.filter(course_id__student_id=student.id).values_list('id', flat=True)

        if serializer.is_valid():
            if int(request.data['teacher_assignment']) in teacher_assignment_list:
                pass
            else:
                return Response({"MSG": "You are not registered in this course"})
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)