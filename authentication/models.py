from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ], blank=True, null=True)
    # country =
    # city =
    facebook_url = models.URLField(blank=True, null=True)
    x_handle = models.CharField(max_length=30, blank=True, null=True)
    instagram_handle = models.CharField(max_length=30, blank=True, null=True)
    tiktok_handle = models.CharField(max_length=24, blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s Profile"
