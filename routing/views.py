from django.db.models import Count
from django.views.generic.base import TemplateView
from spaces.models import Space


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['top_10_spaces'] = Space.objects.annotate(num_followers=Count('followers')).order_by('-num_followers')[:10]
        context['10_verified_spaces'] = Space.objects.filter(verified=True).order_by('created_at')[:10]
        return context


class UserSettings(TemplateView):
    template_name = 'user/settings.html'
