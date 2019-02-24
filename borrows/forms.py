from django import forms
# import re
#
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

from books.models import Book, BookUnit
from settings.models import Course, Batch
from students.models import Student


# class SelectStudentForm(forms.Form):
#     course = forms.ModelChoiceField(
#         widget=forms.Select(attrs={'class': 'form-control select2'}),
#         label="Course",
#         queryset=Course.objects.all(),
#     )
#
#     batch = forms.ModelChoiceField(
#         widget=forms.Select(attrs={'class': 'form-control select2'}),
#         label="Batch",
#         queryset=Batch.objects.none(),
#     )
#
#     student = forms.ModelChoiceField(
#         label='Student',
#         widget=forms.Select(attrs={'class': 'form-control select2'}),
#         queryset=Student.objects.none(),
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.fields['course'].empty_label = 'Select'
#         self.fields['batch'].empty_label = 'Select Batch'
#         self.fields['student'].empty_label = 'Select Student'
#
#         if 'course' in self.data:
#             try:
#                 course = int(self.data.get('course'))
#                 self.fields['batch'].queryset = Batch.objects.filter(course=course).order_by(
#                     'name')
#             except (ValueError, TypeError):
#                 pass
#
#         if 'batch' in self.data:
#             try:
#                 batch = int(self.data.get('batch'))
#                 self.fields['student'].queryset = Student.objects.filter(course_batch__batch=batch).order_by(
#                     'name')
#             except (ValueError, TypeError):
#                 pass
#         # elif self.data.get('course'):
#         #     self.fields['batch'].queryset = self.instance.course.batch_set.order_by('name')
#
#     # def clean(self):
#     #     return self.cleaned_data

class SelectStudentForm(forms.Form):
    student = forms.CharField(
        label='Roll No.',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )


class AssignBookForm(forms.Form):
    book_category = forms.ModelChoiceField(
        label="Book",
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
    )

    book_unit = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Book Unit",
        queryset=BookUnit.objects.none(),
    )

    course = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Course",
        queryset=Course.objects.all(),
    )

    batch = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label="Batch",
        queryset=Batch.objects.none(),
    )

    student = forms.ModelChoiceField(
        label='Student',
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        queryset=Student.objects.none(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['book_category'].empty_label = 'Select'
        self.fields['book_unit'].empty_label = 'Book Unit'
        self.fields['course'].empty_label = 'Select'
        self.fields['batch'].empty_label = 'Select Batch'
        self.fields['student'].empty_label = 'Select Student'

    # def clean_student(self):
    #     roll_no = self.cleaned_data.get('student')
    #     reg = re.compile(r'^[a-zA-Z]+-\d{3}-\d+$')
    #     if reg.match(roll_no):
    #         return roll_no
    # 
    #     raise ValidationError(_('Incorrect format of Roll Number. It must be in format of [a-zA-z]-[0-9]{3}-[0-9].'))

    def clean(self):
        return self.cleaned_data
