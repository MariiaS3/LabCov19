from django.conf import settings
from rest_framework import  viewsets
from .serializers import  DoctorSerializer, PatientSerializer, SpecalizationSerializer, VisitSerializer
from .models import  Doctor, Patient, Specialization, Visit
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse  
from .task import task_send_email
import json
from django.core.mail import send_mail

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

# class MailView(viewsets.ViewSet):
#     def send(request):
#         json_data = json.loads(request.body)
#         print(json_data)
#         task = task_send_email(json_data['subject'], json_data['message'], json_data['send_to'])
#         return HttpResponse("Mail is being sent!")
 
  
  

   