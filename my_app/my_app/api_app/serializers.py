from rest_framework import serializers
from .models import Nurse
from rest_framework import serializers
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = (
            'username',
            'email',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token

