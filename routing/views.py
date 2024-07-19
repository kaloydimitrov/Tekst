from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = 'index.html'


class UserSettings(TemplateView):
    template_name = 'user/settings.html'
