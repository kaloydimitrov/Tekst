from .views import SignUpView, SignInView, SignOutView, account_activation_sent, activate, ResetPasswordView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('account-activation-sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='authentication/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='authentication/password-reset-complete.html'),
         name='password_reset_complete'),
]
