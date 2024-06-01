from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Name', 'class': 'form-control', 'v-model': 'name'}
        ))

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Enter content', 'class': 'form-control', 'v-model': 'content'}
        ))

    visibility = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input', 'id': 'flexSwitchCheckDefault'}
        ),
        required=False,
        initial=True
    )

    class Meta:
        model = Post
        fields = ['name', 'content', 'visibility']
