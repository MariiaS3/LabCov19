from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.
class LablUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=10, blank=False)
    token = models.CharField(max_length=600, unique=True, null=True)
    is_active = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    class Meta:
        abstract=True

class Nurse(LablUser):
    pass
# 'log', models.BooleanField(default=True)),
class Visit(models.Model):
    date = models.DateField() #data wizyty
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


class Results(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    messenge = models.CharField(max_length=600)
    VACCINE_CHOICE = (  # czy byl zaszczepiony
        ('Y', 'YES'),
        ('N', 'NO'), 
    )
    vaccine = models.CharField(max_length=1, choices=VACCINE_CHOICE)
    TEST_CHOICE = (  # czy byl zaszczepiony
        ('P', 'POSITIVE'),
        ('N', 'NEGATIVE'),
    )
    results =models.CharField(max_length=1, choices=TEST_CHOICE)
