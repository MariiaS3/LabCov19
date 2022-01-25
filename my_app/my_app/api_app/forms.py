from django import forms
from .models import Visit

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            'data',
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'phone_number',
            'gender',
            'do_you_want_vaccine'
        ]
