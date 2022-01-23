from rest_framework import serializers
from .models import Nurse, Visit
from rest_framework import serializers
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .task import task_send_email

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
        task = task_send_email('Wyniki','wszystko dobrze zyjesz',instance.email)
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

