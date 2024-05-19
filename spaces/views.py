from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Space
from .forms import CreateSpaceForm


class SpaceCreateView(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    model = Space
    template_name = 'spaces/create-space.html'
    form_class = CreateSpaceForm
    success_message = 'Your space was created successfully'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


# TODO: https://chatgpt.com/c/9f37bbdb-cff3-493c-a5fb-0bf0940bc6d1
