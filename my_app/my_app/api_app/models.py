from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.
class LablUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    token = ""
    objects = UserManager()
    USERNAME_FIELD = 'username'
    class Meta:
        abstract=True

class Nurse(LablUser):
    pass



class Visit(models.Model):
    data = models.DateField() #data wizyty
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    VACCINE_CHOICE = (  # czy chce sie szczepic
        ('Y', 'YES'),
        ('N', 'NO'),
    )
    do_you_want_vaccine = models.CharField(max_length=1, choices=VACCINE_CHOICE)