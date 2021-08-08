from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    short_intro = models.CharField(blank=True, null=False, max_length=200)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        blank=True,
        null=True,
        upload_to="profiles/",
        default="profiles/user-default.png",
    )
    social_github = models.CharField(blank=True, null=False, max_length=100)
    social_linkedin = models.CharField(blank=True, null=False, max_length=100)
    social_instagram = models.CharField(blank=True, null=False, max_length=100)
    social_twitter = models.CharField(blank=True, null=False, max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.username)


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True, max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)