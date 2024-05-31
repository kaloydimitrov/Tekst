from django.urls import path
from .views import SpaceCreateView, SpaceListView

urlpatterns = [
    path('create/', SpaceCreateView.as_view(), name='create_space'),
    path('list/', SpaceListView.as_view(), name='list_spaces')
]
