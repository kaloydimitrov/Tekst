from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from unidecode import unidecode

User = get_user_model()


class Profile(models.Model):
    ONLY_ME = 'M'
    FOLLOWERS = 'F'
    PUBLIC = 'P'
    DISPLAY_CHOICES = (
        (ONLY_ME, "Само аз"),
        (FOLLOWERS, "Само последователи"),
        (PUBLIC, "Публично"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ], blank=True, null=True)
    country = models.CharField(max_length=30, default='България', blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    x_handle = models.CharField(max_length=30, blank=True, null=True)
    instagram_handle = models.CharField(max_length=30, blank=True, null=True)
    tiktok_handle = models.CharField(max_length=24, blank=True, null=True)
    visibility = models.CharField(max_length=1, choices=DISPLAY_CHOICES, default=PUBLIC)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(unidecode(self.user.username))
            self.slug = slug
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s Profile"


class UserFollows(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['following', 'follower'], name='unique_following_follower')
        ]


class UserReport(models.Model):
    REPORT_TYPES = [
        ('SPAM', 'Спам'),
        ('INAPPROPRIATE', 'Неподходящо съдържание'),
        ('HARASSMENT', 'Обида'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'В процес'),
        ('RESOLVED', 'Готово'),
        ('REJECTED', 'Отхвърлено'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    reported_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-reported_on']
        verbose_name = "User Report"
        verbose_name_plural = "User Reports"

    def __str__(self):
        return f"{self.report_type} report by {self.reporter} on {self.reported_user} - Status: {self.status}"
