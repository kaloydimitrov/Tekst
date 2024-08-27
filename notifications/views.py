from django.views.generic.list import ListView
from .models import Notification


class UserListNotifications(ListView):
    model = Notification
    template_name = 'user/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self, *args, **kwargs):
        queryset = super(UserListNotifications, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-timestamp')
        queryset.filter(is_read=False).update(is_read=True)
        return queryset
