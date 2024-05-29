from django import forms
from .models import Space, Tag
from django.core.exceptions import ValidationError


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
        widget=forms.Textarea(
            attrs={'placeholder': 'Enter description', 'class': 'form-control'}
        ))

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control'}
        ))

    class Meta:
        model = Space
        fields = ['name', 'description', 'image']

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
