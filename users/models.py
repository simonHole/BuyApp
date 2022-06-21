from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    # every user have to have on_delete attribute
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    biography = models.TextField(null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='profiles/default.png')
    github = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    site = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.nickname)


class Technology(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
