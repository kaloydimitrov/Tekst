from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from .forms import CreateSpaceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Space, UserSpaceFollow, Tag


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
    paginate_by = 12

    def get_queryset(self):
        order = self.request.GET.get('order')

        if order == 'newest':
            return Space.objects.all().order_by('-created_at')
        elif order == 'oldest':
            return Space.objects.all().order_by('created_at')

        return Space.objects.all().order_by('name')

    def get_context_data(self, *args, **kwargs):
        context = super(SpaceListView, self).get_context_data(*args, **kwargs)
        context['name'] = self.request.GET.get('name')
        context['content'] = self.request.GET.get('content')
        followed_spaces = UserSpaceFollow.objects.filter(user=self.request.user).values_list('space_id', flat=True)
        context['followed_spaces'] = followed_spaces
        return context


class SpaceDetailView(DetailView, LoginRequiredMixin):
    template_name = 'spaces/space-details.html'
    model = Space

    def get_context_data(self, *args, **kwargs):
        context = super(SpaceDetailView, self).get_context_data()
        space = self.get_object()
        context['is_following'] = UserSpaceFollow.objects.filter(user=self.request.user, space=space).exists()
        context['tags'] = Tag.objects.filter(space=space)
        return context
