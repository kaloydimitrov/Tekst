from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import CreateSpaceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Space


class SpaceCreateView(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    template_name = 'spaces/create-space.html'
    form_class = CreateSpaceForm
    success_message = 'Space successfully created'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class SpaceListView(ListView, LoginRequiredMixin):
    template_name = 'spaces/list-spaces.html'
    model = Space

    def get_context_data(self, *args, **kwargs):
        context = super(SpaceListView, self).get_context_data(*args, **kwargs)
        name_param = self.request.GET.get('name')
        content_param = self.request.GET.get('content')
        context['name'] = name_param
        context['content'] = content_param
        return context
