from rest_framework import serializers
from .models import Employee, Department, Leave

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Employee
        fields = '__all__'

class LeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = Leave
        fields = '__all__'
