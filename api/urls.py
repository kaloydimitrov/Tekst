from django.urls import path
from .views import SpaceAPIView

urlpatterns = [
    path('space/', SpaceAPIView.as_view(), name='create_space')
]
