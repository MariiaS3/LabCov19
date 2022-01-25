from atexit import register
from django.conf import settings
from rest_framework import  viewsets
from .serializers import  NurseSerializer, VisitSerializer
from .models import  Nurse, Visit
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse  
from .task import task_send_email
import json
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from django.shortcuts import render, redirect 
from django.contrib.auth import  login, logout
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .forms import VisitForm

class Login(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return render(request, "signin.html",{})#Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST.get('email')
            password =request.POST.get('password')
            print(email)
            user = None
                # if the email has been passed
            if '@' in email:
                user = Nurse.objects.filter(Q(email=email) & Q(password=password)).distinct()
                if not user.exists():
                    messages.info(request, 'Username OR password is incorrect')
                    return  render(request, 'signin.html', {})
                user = Nurse.objects.get(email=email)
            else:
                user = Nurse.objects.filter(Q(username=email) & Q(password=password)).distinct()
                if not user.exists():
                    messages.info(request, 'Username OR password is incorrect')
                    return  render(request, 'signin.html', {})
                user = Nurse.objects.get(username=email)
            refresh = RefreshToken.for_user(user)
            user.token = str(refresh.access_token)
            user.save()
            print(user.token)
            return render(request, 'cookies.html', {'token': user.token})
        return render(request, 'signin.html', {})



def Logout(request):
    return redirect('login')
  
# @login_required(login_url='login')
def visitsList(request):
    visits = Visit.objects.all()

    return render(request, 'visits.html', {'visits':visits})

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class NurseViews(generics.GenericAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer

    def get(self, request, *args, **kwargs):
        return render(request, "signup.html", {})

    def post(self, request, *args, **kwargs):
        print(Nurse.objects.all())
        if request.method == 'POST':
            print(request.data)
            serializer_class = NurseSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                messages.success(request, 'Account created :) Please now log in.')
                return  redirect('login')
            else:
                return render(request, 'signup.html', {})
        return render(request, 'signup.html', {})



class VisitViews(generics.GenericAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
     
    def get(self, request, *args, **kwargs):
        return render(request, "signup.html", {})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print(request.data)
            serializer_class = VisitSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                serializer_class.save()
                messages.success(request, '.....')
                return  redirect('login')
            else:
                return render(request, 'signup.html', {})
        return render(request, 'signup.html', {})

    # def get_queryset(self):
    #     spec_id = self.request.query_params.get('spec_id')
    #     return Visit.objects.filter(doctor__specialization__id = spec_id).distinct()

def widok(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return HttpResponse("<h1>Widok <br> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum</h1>")

    
def template(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return render(request, "signin.html",{})


def main(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return render(request, "index.html",{})


def visit(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return render(request, "visit.html",{})

def NewVisit(request):
    form = VisitForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True) #zapisz do bazy
        form=VisitForm() # refresh

    context = {
        'form' : form
    }

    return render(request,"newvisit.html", context)
