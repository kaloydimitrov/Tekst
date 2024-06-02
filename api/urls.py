from django.urls import path
from django.urls import include
from .views import SpaceDetailView, SpaceListView

urlpatterns = [
    path('space/', include([
        path('all/', SpaceListView.as_view(), name='get_all_spaces'),
        path('<int:pk>/', SpaceDetailView.as_view(), name='get_space_details'),
    ])),

]
