from django.urls import path
from .views import SpaceCreateView

urlpatterns = [
    path('create/', SpaceCreateView.as_view(), name='create_space')
]
