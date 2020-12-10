from django.contrib.auth.models import User
from rest_framework import serializers
from hospital_automation.models import User_type, Patient, Patient_history, Helpers_nurses, Medicines

# making a user serializer
class PatientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only = True)
    last_name = serializers.CharField(read_only = True)
    guardian_name = serializers.CharField(read_only = True)
    problem_name = serializers.CharField(read_only = True)
    assigned_doctor = serializers.CharField(read_only = True)
    class Meta:
        model = Patient
        fields = ['id','first_name', 'last_name','guardian_name','problem_name','assigned_doctor']

class GetPatientName(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only = True)
    last_name = serializers.CharField(read_only = True)
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name']

class Patient_historySerializer(serializers.ModelSerializer):
    patient_name = PatientSerializer(read_only = True)
    class meta:
        model = Patient_history
        fields = ['patient_name']