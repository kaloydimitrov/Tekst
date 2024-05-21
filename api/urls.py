from django.urls import path
from .views import SpaceAPIView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('space/create/', SpaceAPIView.as_view(), name='create_space'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
