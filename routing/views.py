from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = 'index.html'


class UserInfo(TemplateView):
    template_name = 'user/info.html'

    def get_context_data(self, **kwargs):
        context = super(UserInfo, self).get_context_data(**kwargs)
        context['user'] = self.request.user
