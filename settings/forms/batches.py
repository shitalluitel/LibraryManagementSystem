from django import forms
from settings.models import Batch


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch

        fields = ['name', 'code']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Batch Name',
            'code': 'Batch Code',
        }

