from django.conf import settings
from .serializers import  NurseSerializer
from .models import  Nurse, Results, Visit
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse  
from .task import task_send_email
from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render, redirect 
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .forms import ResultsForm, VisitForm
import re


#main page 
def main(request,*args,**kwargs):
    user =  Nurse.objects.filter(is_active=True) 
    if user:
        nurse =  Nurse.objects.get(is_active=True) 
        return render(request, "index.html", {'nurse': nurse})
    return render(request, "index.html",{})


#check password
def password_check(password):
 length_error = len(password) < 8 #
 digit_error = re.search(r"\d", password) is None 
 uppercase_error = re.search(r"[A-Z]", password) is None 
 lowercase_error = re.search(r"[a-z]", password) is None 
 symbol_error = re.search(r"[ !#$@%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None 
 password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error ) 
 
 return {
 'password_ok' : password_ok,
 'length_error' : length_error,
 'digit_error' : digit_error,
 'uppercase_error' : uppercase_error,
 'lowercase_error' : lowercase_error,
 'symbol_error' : symbol_error,
 }

# Register
class Register(generics.GenericAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer

    def get(self, request, *args, **kwargs):
        return render(request, "signup.html", {})

    def post(self, request, *args, **kwargs):
        print(Nurse.objects.all())
        if request.method == 'POST':
            email = request.data['email']
            password = request.data['password']
            password2 = request.data['password2']
            if '@' in email:
                haslo=password_check(password)
                if haslo['password_ok']:
                    if password == password2:    
                        serializer_class = NurseSerializer(data=request.data)
                        if serializer_class.is_valid(raise_exception=True):
                            serializer_class.save()
                            messages.info(request, 'Account created :) Please now log in.')
                            return  redirect('login')
                        else:
                            messages.info(request, 'Something wrong')
                            return render(request, 'signup.html', {})
                    else:
                        messages.info(request, 'Passwords vary')
                        return render(request, 'signup.html', {})
                message = ""
                if  haslo['length_error']:
                    message += "Password contains at least 8 characters\n"
                if  haslo['digit_error']:
                    message += "Password contains at least one digit character\n"
                if  haslo['uppercase_error']:
                    message += "Password contains at least one upper character\n"
                if  haslo['lowercase_error']:
                    message += "Password contains at least one lower character\n"
                if  haslo['symbol_error']:
                    message += "Password contains at least one special character\n"  
                print(message)
                messages.info(request, message)
                return render(request, 'signup.html', {})
            else:
                messages.info(request, 'Email is incorrect')
                return render(request, 'signup.html', {})
        return render(request, 'signup.html', {})

#login
class Login(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return render(request, "signin.html",{})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST.get('email')
            password =request.POST.get('password')
            print(email)
            user = None
            if '@' in email:
                user = Nurse.objects.filter(Q(email=email) & Q(password=password)).distinct()
                if not user.exists():
                    messages.info(request, 'Email OR password is incorrect')
                    return  render(request, 'signin.html', {})
                user = Nurse.objects.get(email=email)
            else:
                messages.info(request, 'Email OR password is incorrect')
                return  render(request, 'signin.html', {})
            refresh = RefreshToken.for_user(user)
            user.token = str(refresh.access_token)
            user.is_active = True
            user.save()
            print(user.token)
            return render(request, 'cookies.html', {'token': user.token})
        return render(request, 'signin.html', {})

#logout
def Logout(request):
    user =  Nurse.objects.filter(is_active=True) 
    if user:
        nurse =  Nurse.objects.get(is_active=True) 
        nurse.is_active = False
        nurse.token = ""
        nurse.save()
    return redirect('login')
  
#list of patient visits
def visitsList(request):
    user =  Nurse.objects.filter(is_active=True) 
    if user:
        nurse =  Nurse.objects.get(is_active=True)
        email = list(request.GET)
        if email == []:
            visits = Visit.objects.all()
            return render(request, 'visits.html', {'visits':visits, 'nurse': nurse})
        else:
            Results.objects.all().delete()
            visit = Visit.objects.get(email=email[0])
            Results.objects.create(email=visit.email, first_name=visit.first_name,last_name=visit.last_name,phone_number=visit.phone_number,vaccine=visit.do_you_want_vaccine) 
            Visit.objects.filter(email=email[0]).delete()          
            return redirect( 'results')
    return render(request, 'visits.html', {})

#Register for a new visit
def NewVisit(request):
    form = VisitForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=True) #zapisz do bazy
            email = form.cleaned_data['email']
            name = form.cleaned_data['first_name']
            date = str(form.cleaned_data['date'])
            task_send_email('Your new visit','Hi '+name+',\n\n'+'Thank you for registering in LabCov19.\n The day of your visit is '+date+ '.\n\nWe hope your visit will be nice.\n Feel free to ask any questions.\n',email)
            form=VisitForm() # refresh
            messages.success(request, 'Successfully registered.')
        else:
            messages.error(request, 'Something wrong')
    
    context = {
        'form' : form
    }

    return render(request,"newvisit.html", context)

#send test results
def SendResults(request):
    form = ResultsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['first_name']
            test = form.cleaned_data['results']
            vaccine = form.cleaned_data['vaccine']
            message = form.cleaned_data['messenge']
            if test == 'N' and vaccine=='Y':
                task_send_email('Results','Hello '+name+',\nYour test your test is ready, your test result is: NEGATIVE \n Thank you for vaccinating with us.\nYou also have a message from the nurse '+message,email)
            elif test == 'N' and vaccine=='N':
                task_send_email('Results','Hello '+name+',\nYour test your test is ready, your test result is: NEGATIVE \n We encourage you to vaccinate yourself.\nYou also have a message from the nurse '+message,email)
            elif test == 'P':
                task_send_email('Results','Hello '+name+',\nYour test your test is ready, your test result is: POSITIVE \nWe wish you a quick recovery and encourage you to vaccinate yourself.\nYou also have a message from the nurse '+message,email)
            return redirect("visits")
        else:
            messages.error(request, 'Something wrong')

    visit = list(Results.objects.all())
    if visit==[]:
        print(visit)
    else:
        form = ResultsForm(initial={'email': visit[0].email,'first_name':visit[0].first_name,'last_name':visit[0].last_name,'phone_number':visit[0].phone_number,'vaccine':visit[0].vaccine})
    context = {
        'form' : form
    }
    return render(request,"results.html", context)
    


#=================================================================#
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


def widok(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return HttpResponse("<h1>Widok <br> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum</h1>")

    
def template(request,*args,**kwargs):
    print("Zalogowany jako: ", request.user)
    return render(request, "signin.html",{})


