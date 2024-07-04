from django.core.exceptions import ValidationError
from django import forms
from .models import Post
from spaces.models import Space, Tag


class CreatePostForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'id': 'tags-input', 'v-model': 'tags'}
        ),
        required=False
    )

    space = forms.ModelChoiceField(
        queryset=Space.objects.all(),
        widget=forms.HiddenInput(
            attrs={'id': 'space-select', 'v-model': 'spaceInput'}
        ),
        required=False
    )

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
        fields = ['name', 'content', 'visibility', 'space']

    def save(self, commit=True):
        instance = super(CreatePostForm, self).save(commit=False)
        tags = self.cleaned_data.get('tags', '')

        if commit:
            instance.save()

        if tags:
            try:
                list_tags = tags.split(",")
                for tag_id in list_tags:
                    tag = Tag.objects.get(id=tag_id)
                    tag.post.add(instance)
            except Exception as e:
                raise ValidationError(f'Invalid tags: {e}')

        if commit:
            instance.save()
        return instance
