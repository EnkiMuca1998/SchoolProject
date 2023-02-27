from rest_framework import serializers
from school.models import TeacherAssignment, Assignment

class TeacherAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherAssignment
        fields = ['assnum', 'course_id', 'teacher_id']


class AssignmentGradeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Assignment
        fields = ['id', 'student_id', 'teacher_assignment', 'file', 'score', 'score_in_percentage']
        read_only_fields = ['student_id', 'file', 'teacher_assignment', 'score_in_percentage']


class AssignmentGradeSpecificSerializer(serializers.ModelSerializer):


    class Meta:
        model = Assignment
        fields = ['id', 'score', 'student_id', 'teacher_assignment', 'file', 'score_in_percentage']
        read_only_fields = ['student_id', 'file', 'teacher_assignment', 'id', 'score_in_percentage']


class TeacherStudentListSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=120)
    assignment = serializers.ListField()
    score = serializers.ListField()
    progress = serializers.CharField()

class TeacherCourseListSerializer(serializers.Serializer):

    course_name = serializers.CharField(max_length=120)
    students = TeacherStudentListSerializer(many=True, read_only=True)


