from django import forms

from settings.models import Setting


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = [
            'renew_days',
            'fine_amount',
            'books_allowed',
        ]

        labels = {
            'renew_days': "Book Renew Day",
            'fine_amount': 'Fine Amount',
            'books_allowed': 'No. of Books Allowed',
        }

        widgets = {
            'renew_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'fine_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'books_allowed': forms.NumberInput(attrs={'class': 'form-control'}),
        }
