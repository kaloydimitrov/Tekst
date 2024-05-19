from django.contrib import admin
from django.urls import path, include
from .views import PostCreateView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
]
