from django import forms
from djangoformsetjs.utils import formset_media_js

from settings.models import Course, Batch
from students.models import Student


class CreateChoiceForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label="Select Course",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    batch = forms.ModelChoiceField(
        queryset=Batch.objects.none(),
        label="Select Batch",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['course'].empty_label = 'Select Course'
        self.fields['batch'].empty_label = 'Select Batch'
        self.fields['course'].queryset = Course.objects.all()
        # self.fields['batch'].queryset = Batch

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['batch'].queryset = Batch.objects.filter(course__id=course_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass
        # elif self.instance.pk:
        #     self.fields['batch'].queryset = self.instance.course.batch_set.order_by('name')


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student

        fields = ['name', 'dob', 'phone_no', 'address', 'photo']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control formset-field'}),
            'dob': forms.TextInput(attrs={'class': 'form-control formset-field'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control formset-field'}),
            'address': forms.TextInput(attrs={'class': 'form-control formset-field'}),
            # 'photo': forms.FileField(),
        }

    class Media(object):
        js = formset_media_js + ()
