from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null':True, 'blank': True}

class User(AbstractUser):
    username = None
    verification_token = models.CharField(max_length=50, **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=40, verbose_name='телефон',**NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []