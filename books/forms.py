from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book

        fields = [
            'name',
            'edition',
            'author',
            'publisher',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'edition': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
        }

