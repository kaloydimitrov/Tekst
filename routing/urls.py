from django.urls import path, include
from routing.views import home

urlpatterns = [
    path('', home, name='home')
]
