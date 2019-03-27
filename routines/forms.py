from django import forms

from settings.models import Course, Batch
from .models import Routine


class RoutineDataForm(forms.ModelForm):
    class Meta:
        model = Routine

        fields = [
            'day',
            'time_from',
            'time_to',
            'teacher',
            'subject',
        ]

        widgets = {
            'day': forms.Select(attrs={'class': 'form-control formset-field'}),
            'time_from': forms.TextInput(
                attrs={'class': 'form-control formset-field timepicker', 'placeholder': '10 : 07 AM'}),
            'time_to': forms.TextInput(
                attrs={'class': 'form-control formset-field timepicker', 'placeholder': '11 : 07 AM'}),
            'teacher': forms.TextInput(attrs={'class': 'form-control formset-field'}),
            'subject': forms.TextInput(attrs={'class': 'form-control formset-field'}),
        }


class RoutineCourseBatchForm(forms.ModelForm):
    class Meta:
        model = Routine

        fields = [
            'course',
            'batches',
            'semester',
        ]

        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batches': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RoutineCourseBatchForm, self).__init__(*args, **kwargs)

        self.fields['course'].queryset = Course.objects.all()
        self.fields['batches'].queryset = Batch.objects.none()
        self.fields['course'].empty_label = 'Select Course'
        self.fields['batches'].empty_label = 'Select Batch'

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['batches'].queryset = Batch.objects.filter(course_batches__course_id=course_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['batches'].queryset = self.instance.course.batch_set.all()
