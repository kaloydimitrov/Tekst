from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return

    def get_success_url(self):
        return reverse_lazy('home')


class SignInView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_message = "You have been logged in successfully"

    def get_success_url(self):
        return reverse_lazy('home')


class SignOutView(SuccessMessageMixin, LogoutView):
    success_message = "You have been logged out successfully"

    def get_success_url(self):
        return reverse_lazy('home')
