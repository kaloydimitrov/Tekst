from django.urls import path
from .views import SpaceDetail

urlpatterns = [
    path('space/<int:pk>/', SpaceDetail.as_view(), name='get_space_details')
]
