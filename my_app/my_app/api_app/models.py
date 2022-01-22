from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class LablUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    token = ""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    class Meta:
        abstract=True

class Nurse(LablUser):
    #specialization = models.ManyToManyField(Specialization)
    pass

class Patient(LablUser):
    pass


class Visit(models.Model):
    # nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    data = models.DateField() #data wizyty
    # location = models.CharField(max_length=50) jestesmy biedne i mamy jedna placowke XDDD
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # patient = models.OneToOneField(Patient,on_delete=models.PROTECT, related_name='Patient',null=True,blank=True)
    VACCINE_CHOICE = (  # czy chce sie szczepic
        ('Y', 'YES'),
        ('N', 'NO'),
    )
    do_you_want_vaccine = models.CharField(max_length=1, choices=VACCINE_CHOICE)