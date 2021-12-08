from django.contrib.auth.models import User
from rest_framework import  viewsets
from rest_framework.serializers import Serializer
from .serializers import DoctorSerializer, PatientSerializer, SpecalizationSerializer, VisitSerializer
from .models import Doctor, Patient, Specialization, Visit
from django.core.mail import send_mail
from django.conf import settings
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse  

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class DoctorViews(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    authentication_classes = []
    serializer_class = DoctorSerializer
    # permission_classes = [permissions.IsAuthenticated]'

class PatientViews(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    authentication_classes = []
    serializer_class = PatientSerializer
    # permission_classes = [permissions.IsAuthenticated]

class SpecializationViews(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    authentication_classes = []
    serializer_class = SpecalizationSerializer

class VisitViews(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    authentication_classes = []
    serializer_class = VisitSerializer

    def get_queryset(self):
        spec_id = self.request.query_params.get('spec_id')
        return Visit.objects.filter(doctor__specialization__id = spec_id).distinct()

       
    # def my_mail(request):  
    #     subject = "Greetings from Programink"  
    #     msg     = "Learn Django at Programink.com"  
    #     to      = "mariia.sydor28082001@gmail.com"  
    #     res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    #     if(res == 1):  
    #         msg = "Mail Sent Successfully."  
    #     else:  
    #         msg = "Mail Sending Failed."  
    #     return HttpResponse(msg)  
  

   