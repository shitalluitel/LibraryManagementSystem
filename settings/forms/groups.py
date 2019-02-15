from django import forms
from django.contrib.auth.models import Group, Permission


class GroupsCreate(forms.ModelForm):
    permission = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        label="Permissions",
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': 10})
    )
    class Meta:
        model = Group
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

        label = {
            'name': 'Group'
        }
