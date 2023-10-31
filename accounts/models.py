from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=8, default='')
    profile_pic = models.ImageField(blank=True, null=True)
