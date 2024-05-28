from django import forms
from .models import Space, Tag


class CreateSpaceForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=255, required=False, help_text="Enter tags separated by commas",
        widget=forms.Textarea(
            attrs={'placeholder': 'Enter tags', 'class': 'form-control'}
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
