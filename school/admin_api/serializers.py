from rest_framework import serializers
from school.models import Student

class StudentListSerializer(serializers.Serializer):

        student_name = serializers.CharField(max_length=30)
        grade__avg = serializers.FloatField()


class StudentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class StudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'approved']
