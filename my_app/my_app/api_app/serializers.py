from rest_framework import serializers
from .models import Doctor, Patient, Specialization, Visit
from rest_framework import serializers
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .task import task_send_email


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
         model = Doctor
         fields = '__all__'
         extra_kwargs = {'password': {'write_only': True}}


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class SpecalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # validated_data['doctor'] = self.context['request'].user
        instance = super().create(validated_data)
        task = task_send_email('Wyniki','wszystko dobrze zyjesz',instance.patient.email)
        return instance
   
    class Meta:
         model = Visit
         fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token