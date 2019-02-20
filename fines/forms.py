from django import forms

from fines.models import Fine


class FineStudentForm(forms.Form):
    student = forms.CharField(
        label="Roll No.",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )


class FineForm(forms.ModelForm):
    pay_amount = forms.DecimalField(
        label='Pay',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
    )

    class Meta:
        model = Fine

        fields = [
            'amount'
        ]

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control disabled'})
        }

        labels = {
            'amount': 'Total Fine',
        }
