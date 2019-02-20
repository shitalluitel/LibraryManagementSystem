from django import forms
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from books.models import Book, BookUnit


class SelectStudentForm(forms.Form):
    roll_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_roll_no(self):
        roll_no = self.cleaned_data.get('roll_no')
        reg = re.compile(r'^[a-zA-Z]+-\d{3}-\d+$')
        if reg.match(roll_no):
            return roll_no

        raise ValidationError(_('Incorrect format of Roll Number. It must be in format of [a-zA-z]-[0-9]{3}-[0-9].'))


class AssignBookForm(forms.Form):
    book_category = forms.ModelChoiceField(
        label="Book",
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    book_unit = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Book Unit",
        queryset=BookUnit.objects.none(),
    )

    student = forms.CharField(
        label='Student Roll No.',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['book_category'].empty_label = 'Select'
        self.fields['book_unit'].empty_label = 'Select'

    def clean_student(self):
        roll_no = self.cleaned_data.get('student')
        reg = re.compile(r'^[a-zA-Z]+-\d{3}-\d+$')
        if reg.match(roll_no):
            return roll_no

        raise ValidationError(_('Incorrect format of Roll Number. It must be in format of [a-zA-z]-[0-9]{3}-[0-9].'))

    def clean(self):
        return self.cleaned_data
