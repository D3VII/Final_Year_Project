from django.db import models
from django.contrib.auth.models import User

from .user_type_map import USER_MAP


# Create your models here.
class User_type(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    flag = models.IntegerField()
    specialization = models.CharField(max_length=1200, default='NULL')

    class Meta:
        ordering = ['flag']

    def __str__(self):
        return "user: " + self.user.username + " type: " + USER_MAP[self.flag]


class Patient(models.Model):
    first_name = models.CharField(max_length=1200)
    last_name = models.CharField(max_length=1200)
    guardian_name = models.CharField(max_length=1200)
    city = models.CharField(max_length=1200, default='NULL')
    state = models.CharField(max_length=1200, default='NULL')
    country = models.CharField(max_length=1200, default='NULL')
    country_code = models.CharField(max_length=120, default='+91')
    zip_code = models.CharField(max_length=120, default='NULL')
    phone_number = models.CharField(max_length=1200)
    date = models.CharField(max_length=120, default='NULL')
    address = models.CharField(max_length=1200)
    problem_name = models.CharField(max_length=1200)
    assigned_doctor = models.CharField(max_length=1200)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Patient_history(models.Model):
    user = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='user')
    date = models.DateField()
    diagnosis = models.CharField(max_length=12000)
    blood_pressure = models.CharField(max_length=1200, default='NULL')
    weight = models.CharField(max_length=1200, default='NULL')
    sugar = models.CharField(max_length=1200, default='NULL')
    medicine = models.CharField(max_length=1200)
    morning_intake = models.BooleanField(default=False)
    afternoon_intake = models.BooleanField(default=False)
    evening_intake = models.BooleanField(default=False)
    days = models.IntegerField()
    tests = models.CharField(max_length=1200)
    is_done_with_dispensary = models.BooleanField(default=False)
    is_done_with_test = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Helpers_nurses(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    flag = models.IntegerField()
    contact = models.CharField(max_length=12)
    allotted_doctor = models.CharField(max_length=120)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Medicines(models.Model):
    name = models.CharField(max_length=120)
    price = models.IntegerField()

    def __str__(self):
        return self.name
