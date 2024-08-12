from django.urls import path, include
from routing.views import Home, UserProfile, UserInfoEdit

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('user/', include([
        path('edit/', UserInfoEdit.as_view(), name='user_edit'),
        path('profile/<slug:slug>/', UserProfile.as_view(), name='user_profile')
    ]))
]
