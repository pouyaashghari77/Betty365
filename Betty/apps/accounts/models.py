from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=150)
    birth_date = models.DateField('Birth Date', blank=True, null=True)
    country = models.CharField('Country', max_length=64, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)
    balance = models.FloatField('Balance', default=0, blank=True, null=True)
    security_question = models.CharField('Security Question', max_length=64, blank=True, null=True)
    security_answer = models.CharField('Security Answer', max_length=64, blank=True, null=True)
