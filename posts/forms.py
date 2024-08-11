import bleach
from bleach.css_sanitizer import CSSSanitizer
import html
from django.core.exceptions import ValidationError
from django import forms
from .models import Post
from spaces.models import Space, Tag

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS = ['p', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'b', 'i', 'u', 's', 'strong',
                                                'em', 'br', 'span']
ALLOWED_ATTRIBUTES = {'*': ['class', 'style'], }
ALLOWED_STYLES = ['color']
css_sanitizer = CSSSanitizer(allowed_css_properties=ALLOWED_STYLES)


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
        ),
        required=False
    )

    content = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'v-model': 'content'}
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

    def clean_content(self):
        content = self.cleaned_data.get('content')
        unescaped_content = html.unescape(content)
        sanitized_content = bleach.clean(unescaped_content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
                                         strip=True, css_sanitizer=css_sanitizer)

        if sanitized_content != unescaped_content:
            raise ValidationError('Your field contains invalid HTML.')

        return content

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
