from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    pesel = models.CharField(max_length=11)
    clinics = models.CharField(max_length=1000, blank=True, null=True)
    chronic_conditions = models.CharField(max_length=1000, blank=True, null=True)
