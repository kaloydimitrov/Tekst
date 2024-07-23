import bleach
from bleach.css_sanitizer import CSSSanitizer
import html
from django import forms
from .models import Space, Tag
from django.core.exceptions import ValidationError

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS = ['p', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'b', 'i', 'u', 's', 'strong',
                                                'em', 'br', 'span']
ALLOWED_ATTRIBUTES = {'*': ['class', 'style'], }
ALLOWED_STYLES = ['color']
css_sanitizer = CSSSanitizer(allowed_css_properties=ALLOWED_STYLES)


class CreateSpaceForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'id': 'tags-input'}
        ))

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Name', 'class': 'form-control'}
        ))

    description = forms.CharField(
        widget=forms.HiddenInput(
            attrs={'v-model': 'descriptionInput'}
        ))

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control', 'id': 'image-field'}
        ))

    class Meta:
        model = Space
        fields = ['name', 'description', 'image']

    def clean_description(self):
        description = self.cleaned_data.get('description')
        unescaped_description = html.unescape(description)
        sanitized_description = bleach.clean(unescaped_description, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
                                             strip=True, css_sanitizer=css_sanitizer)

        if sanitized_description != unescaped_description:
            raise ValidationError('Your field contains invalid HTML.')

        return description

    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get('tags', '')

        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

        if len(tag_list) < 3:
            raise ValidationError("You should provide at least 3 tags.")

        cleaned_data['tags'] = ','.join(tag_list)
        return cleaned_data

    def save(self, commit=True):
        space = super().save(commit=False)
        if commit:
            space.save()
            tags = self.cleaned_data['tags']
            if tags:
                tag_list = [tag.strip() for tag in tags.split(',')]
                for tag_name in tag_list:
                    Tag.objects.create(name=tag_name, space=space)
        return space
