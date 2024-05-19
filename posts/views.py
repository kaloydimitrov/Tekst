from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Post
from .forms import CreatePostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class PostCreateView(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    model = Post
    template_name = 'posts/create-post.html'
    form_class = CreatePostForm
    success_message = 'Your post was created successfully'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')
