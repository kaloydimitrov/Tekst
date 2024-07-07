from Tekst.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm

User = get_user_model()


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'authentication/register.html'
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        html_message = render_to_string('authentication/account-activation-email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=EMAIL_HOST_USER,
            to=[user.email]
        )

        message.attach_alternative(html_message, "text/html")
        message.send()

        return redirect('account_activation_sent')

    def get_success_url(self):
        return reverse_lazy('home')


class SignInView(SuccessMessageMixin, LoginView):
    template_name = 'authentication/login.html'
    form_class = UserLoginForm
    success_message = "You have been logged in successfully"

    def get_success_url(self):
        return reverse_lazy('home')


class SignOutView(SuccessMessageMixin, LogoutView):
    success_message = "You have been logged out successfully"

    def get_success_url(self):
        return reverse_lazy('home')


def account_activation_sent(request):
    return render(request, 'authentication/account-activation-sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('home')
    else:
        return render(request, 'authentication/account-activation-invalid.html')
