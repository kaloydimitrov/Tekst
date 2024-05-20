from django.urls import path
from .views import SpaceCreateTemplateView

urlpatterns = [
    path('create/', SpaceCreateTemplateView.as_view(), name='create_space_template')
]
