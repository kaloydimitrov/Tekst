from django.contrib import admin
from django.urls import path, include
from .views import PostCreateView, PostDetailView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_details'),
]
