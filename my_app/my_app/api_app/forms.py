from django import forms
from .models import  Results, Visit


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

class ResultsForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'vaccine',
            'results',
            'messenge'
        ]