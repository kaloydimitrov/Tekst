from .views import SignUpView, SignInView, SignOutView
from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout')
]
