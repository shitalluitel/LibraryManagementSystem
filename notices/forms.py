from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice

        fields = [
            'title',
            'notice',

            # 'type'
        ]

        widgets = {
            # 'type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'notice': CKEditorUploadingWidget(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['type'].empty_label = "Select Type"
