from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book

        fields = [
            'name',
            'code',
            'edition',
            'author',
            'publisher',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'edition': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BookUnitDeleteForm(forms.Form):

    remark = forms.CharField(
        label="Reason for delete action",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'e.g. Book Lost', 'rows': 3})
    )


class BookUnitAddForm(forms.Form):
    units = forms.IntegerField(
        label="No. of Books",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )
