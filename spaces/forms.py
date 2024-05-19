from django import forms
from .models import Space


class CreateSpaceForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Name', 'class': 'form-control'}
        ))

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Enter description', 'class': 'form-control'}
        ))

    class Meta:
        model = Space
        fields = ['name', 'description']
