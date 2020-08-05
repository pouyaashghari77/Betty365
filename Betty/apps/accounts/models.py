from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import F

from Betty.apps.authentication.managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField('Email', max_length=150, unique=True,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=150)
    birth_date = models.DateField('Birth Date', blank=True, null=True)
    country = models.CharField('Country', max_length=64, blank=True, null=True)
    balance = models.FloatField('Balance', default=0, blank=True, null=True)
    security_question = models.CharField('Security Question', max_length=64, blank=True, null=True)
    security_answer = models.CharField('Security Answer', max_length=64, blank=True, null=True)

    username = models.CharField('Username', max_length=32, blank=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def increase_balance(self, amount):
        User.objects.filter(pk=self.pk).update(balance=F('balance') + amount)

    def decrease_balance(self, amount):
        User.objects.filter(pk=self.pk).update(balance=F('balance') - amount)
