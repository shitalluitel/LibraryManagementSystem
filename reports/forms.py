from django import forms
from django.core.exceptions import ValidationError
from model_utils import Choices

from settings.models import Course, Batch
from students.models import Student

STATUS = Choices(
    ('', 'Select Status'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('cancelled', 'Cancelled'),
    ('returned', 'Returned')
)


class BookReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'class': 'form-control datepicker-here', 'data-language': 'en', 'data-date-format': 'yyyy-mm-dd',
                   'placeholder': 'Start Date'}),
        required=False,
    )

    end_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'class': 'form-control datepicker-here', 'data-language': 'en', 'data-date-format': 'yyyy-mm-dd',
                   'placeholder': 'End Date'}),
        required=False,
    )

    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=STATUS,
        required=False
    )

    def clean_start_date(self):
        data = self.cleaned_data
        return data.get('start_date')

    def clean_end_date(self):
        data = self.cleaned_data
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError('Invalid range of date selected.')
            return end_date
        return end_date


class StudentReportForm(forms.Form):
    course = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course",
        queryset=Course.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(StudentReportForm, self).__init__(*args, **kwargs)

        self.fields['course'].empty_label = 'Select Course'
