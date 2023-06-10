from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.timesince import timesince
import os
import datetime

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
