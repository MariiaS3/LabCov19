from rest_framework import serializers
from .models import Doctor, Patient, Specialization, Visit
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User


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