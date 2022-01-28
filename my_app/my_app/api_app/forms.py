from django import forms
from .models import Nurse, Visit
from django.contrib.auth.forms import UserCreationForm

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            'date',
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'phone_number',
            'gender',
            'do_you_want_vaccine'
        ]