from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from spaces.models import Tag
from .models import Post, ReactionType
from .forms import CreatePostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied


class PostCreateView(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    model = Post
    template_name = 'posts/create-post.html'
    form_class = CreatePostForm
    success_message = 'Your post was created successfully'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args, **kwargs)
        context['space_id'] = self.request.GET.get('space_id')
        context['name'] = self.request.GET.get('name')
        context['content'] = self.request.GET.get('content')
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class PostDetailView(DetailView):
    template_name = 'posts/post-details.html'
    model = Post

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        token = self.request.GET.get('token')

        post = get_object_or_404(Post, slug=slug)

        if not post.visibility:
            if not str(post.token) == token:
                raise PermissionDenied('Няма token или е невалиден.')

        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        post = self.get_object()
        context['tags'] = Tag.objects.filter(post=post)
        context['in_post_details'] = True
        context['reaction_types'] = ReactionType.objects.all()
        context['post_reaction_types'] = [r.reaction_type for r in post.reactions.all()]

        return context
