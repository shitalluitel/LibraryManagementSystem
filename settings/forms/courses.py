from django import forms
from settings.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course

        fields = ['name', 'code']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Course Name',
            'code': 'Course Code',
        }

