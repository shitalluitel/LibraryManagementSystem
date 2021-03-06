from django import forms
from .models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File

        fields = [
            'document',
            'title',
            'type'
        ]

        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['type'].empty_label = "Select Type"
