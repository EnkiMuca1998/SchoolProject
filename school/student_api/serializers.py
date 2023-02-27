from rest_framework import serializers
from school.models import Student, Course, StudentCourse, Assignment, Semester, Waitlist, TeacherAssignment

class AddStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id', 'approved', 'user_id']


class StudentDetailSerializer(serializers.Serializer):

    course = serializers.CharField(max_length=50)
    notat = serializers.ListField()
    average = serializers.FloatField()
    progress = serializers.CharField(max_length=50)


class CourseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'coname', 'course_start', 'status', 'teacher_id']


class CourseRegistrationSerializer(serializers.ModelSerializer):
    #user_id = serializers.IntegerField(source='student_id.user_id')

    class Meta:
        model = StudentCourse
        fields = ['student_id', 'course_id']




class WaitlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Waitlist
        fields = '__all__'


class AssignmentListSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='course_id.coname')

    class Meta:
        model = TeacherAssignment
        fields = ['id', 'course', 'course_id', 'assnum', 'teacher_id',]


class AssignmentSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ['file', 'student_id', 'teacher_assignment']