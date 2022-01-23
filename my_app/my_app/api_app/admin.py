from django.contrib import admin
from django.db.models.base import Model
from .models import Nurse, Visit

admin.site.register(Nurse)
admin.site.register(Visit)
