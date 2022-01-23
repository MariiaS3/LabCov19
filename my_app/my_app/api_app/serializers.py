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
         fields = '__all__'
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

class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    email = serializers.CharField()
    password = serializers.CharField()
    # token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        email = data.get("email", None)
        password = data.get("password", None)
        if not email and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in email:
            user = Nurse.objects.filter(Q(email=email) & Q(password=password)).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = Nurse.objects.get(email=email)
        else:
            user = Nurse.objects.filter(Q(username=email) & Q(password=password)).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = Nurse.objects.get(username=email)
            print(user)
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = Nurse
        fields = (
            'email',
            'password',
        )

    def create(self, validated_data):
        user = Nurse(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

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
