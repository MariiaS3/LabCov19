from rest_framework import serializers
from .models import Nurse, Visit
from rest_framework import serializers
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .task import task_send_email
from django.db.models import Q
from django.core.exceptions import ValidationError
from uuid import uuid4

class NurseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nurse
        fields = (
            'username',
            'email',
            'password',
            'phone_number',

        )
        extra_kwargs = {'password': {'write_only': True}}

  


class VisitSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # validated_data['doctor'] = self.context['request'].user
        instance = super().create(validated_data)
        task = task_send_email('Wyniki','wszystko dobrze zyjesz',instance.patient.email)
        return instance
   
    class Meta:
         model = Visit
         fields = '__all__'

#nie dziala testowe
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token

class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = Nurse.objects.get(token=token)
        except Exception as e:
            raise ValidationError(str(e))
        user.token = ""
        user.save()
        return data

    class Meta:
        model = Nurse
        fields = (
            'token',
        )
