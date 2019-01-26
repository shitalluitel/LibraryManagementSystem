from django import forms
from django.forms import ModelMultipleChoiceField

from settings.models import Batch, CourseBatch, Course


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


class CourseBatchCreateForm(forms.Form):
    course = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        label="Choose courses for this batch."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #
    #     self.fields['course'] = ModelMultipleChoiceField(queryset=Course.objects.all())
        self.fields['course'].widget.attrs['class'] = 'form-control'
        self.fields['course'].empty_label = "Choose a countries"
