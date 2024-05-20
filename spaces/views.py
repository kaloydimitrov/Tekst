from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class SpaceCreateTemplateView(TemplateView, LoginRequiredMixin):
    template_name = 'spaces/create-space.html'
