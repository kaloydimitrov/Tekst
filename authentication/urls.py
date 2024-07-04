from .views import SignUpView, SignInView, SignOutView, account_activation_sent, activate
from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('account-activation-sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
