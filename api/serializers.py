from rest_framework_recursive.fields import RecursiveField
from rest_framework import serializers
from .models import Job_title, Employee



class Job_title_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Job_title
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='Job_title.title')
    chief_name = serializers.CharField(source='chief')
    salary = serializers.CharField(source='salaryfunc')

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'second_name', 'middle_name', 'hired', 'salary', 'chief_name', 'username', 'job_title')

class RecurseEmployeeSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='Job_title.title')
    chief_name = serializers.CharField(source='chief')
    salary = serializers.CharField(source='salaryfunc')
    children = serializers.ListField(read_only=True, child=RecursiveField(), source='children.all')

    
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'second_name', 'middle_name', 'hired', 'salary', 'chief_name', 'username', 'job_title', 'children') 