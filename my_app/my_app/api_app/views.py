from django.conf import settings
from rest_framework import  viewsets
from .serializers import  NurseSerializer, PatientSerializer, VisitSerializer, UserLogoutSerializer,UserLoginSerializer
from .models import  Nurse, Patient,  Visit
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse  
from .task import task_send_email
import json
from django.core.mail import send_mail
from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class Login(generics.GenericAPIView):
    # get method handler
    queryset = Nurse.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

class Logout(generics.GenericAPIView):
    queryset = Nurse.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


#nie dziala
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class NurseViews(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    authentication_classes = []
    serializer_class = NurseSerializer
    # permission_classes = [permissions.IsAuthenticated]'

class PatientViews(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    authentication_classes = []
    serializer_class = PatientSerializer
    # permission_classes = [permissions.IsAuthenticated]
#
# class SpecializationViews(viewsets.ModelViewSet):
#     queryset = Specialization.objects.all()
#     authentication_classes = []
#     serializer_class = SpecalizationSerializer

class VisitViews(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    authentication_classes = []
    serializer_class = VisitSerializer

    # def get_queryset(self):
    #     spec_id = self.request.query_params.get('spec_id')
    #     return Visit.objects.filter(doctor__specialization__id = spec_id).distinct()

def widok(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return HttpResponse("<h1>Widok <br> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum</h1>")



def template(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return render(request, "stronka.html",{})




   