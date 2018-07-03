from django.db import models

# Create your models here.


class User(models.Model):
    user_email = models.CharField(max_length=512, default=None, unique=True)
    access_token = models.CharField(max_length=1024, default=None)
    user_id = models.CharField(max_length=255, default=None)
    company_id = models.CharField(max_length=255, default=None)
    active = models.BooleanField(default=True)
