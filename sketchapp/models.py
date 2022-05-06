from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

# Create your models here.

def file_upload(self, filename):
    url = 'data/images'
    return url

class Blog(models.Model):
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.FileField(upload_to=file_upload, blank=True)
    banner = models.FileField(upload_to=file_upload, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.title}"

class Messages(models.Model):
    name = models.TextField(blank=True)
    email = models.TextField(blank=True)
    subject = models.TextField(blank=True)
    message = models.TextField(blank=True)
    def __str__(self):
        return f"{self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="user")
    name = models.TextField(blank=True)
    phone = models.BigIntegerField(default=None)
    image = models.FileField(upload_to=file_upload, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    email = models.TextField(blank=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}"
