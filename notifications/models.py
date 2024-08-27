from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('follow', 'Следване'),
        ('reply', 'Отговор'),
        ('post_created', 'Публикация създадена'),
        ('post_deleted', 'Публикация изтрита'),
        ('space_created', 'Тема създадена'),
        ('space_deleted', 'Тема изтрита'),
    ]

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
    )

    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    extra_data = models.JSONField(null=True, blank=True)
