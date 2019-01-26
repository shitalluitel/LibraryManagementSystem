from django import forms
from django.conf import settings
from django.contrib.auth import password_validation
import re

from settings.models import WardNumber
from .models import User
from users.models import USER_ROLES


class RegisterForm(forms.ModelForm):
    """
    Form to register a new user
    """
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        strip=False,
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password again'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'username',
            'password',
            'confirm_password'
        ]
        widgets = {

            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        full_name = self.cleaned_data['last_name']

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password mismatch')
        if full_name.lower() in password.lower():
            raise forms.ValidationError('Password similar to name of user.')
        password_validation.validate_password(confirm_password, self.instance)
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
            raise forms.ValidationError('Invalid Email format')
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        user.send_confirmation_email()
        return user


class LoginForm(forms.Form):
    """
    Form to login a user
    """
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username or email'}),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        strip=False,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

        if user:
            return user.email
        return None


class PasswordChangeForm(forms.Form):
    """
    Form to change user password
    """
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your current password'}),
        strip=False,
    )

    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password'}),
        strip=False,
    )

    confirm_new_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password password'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Incorrect current password')
        return current_password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError('Password mismatch')
        password_validation.validate_password(confirm_new_password, self.user)
        return confirm_new_password

    def save(self, commit=True):
        password = self.cleaned_data["confirm_new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class SendPasswordResetEmailForm(forms.Form):
    """
    Form to send password reset email
    """
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        super(SendPasswordResetEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        try:
            self.user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise forms.ValidationError("No account associated with this email.")

        return self.cleaned_data['email']

    def save(self):
        if not settings.DEBUG:
            self.user.send_password_reset_email()
        self.user.send_password_reset_email()


class PasswordResetForm(forms.Form):
    """
    Form to reset user's password
    """
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password'}),
        strip=False,
    )

    confirm_new_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password password'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError('Password mismatch')
        return confirm_new_password

    def save(self):
        password = self.cleaned_data["confirm_new_password"]
        self.user.set_password(password)
        self.user.save()
        return self.user


class ProfileForm(forms.ModelForm):
    """
    Form to edit user profile
    """

    class Meta:
        model = User
        fields = [
            'full_name',
            # 'username',
            'email',
        ]
        widgets = {

            # 'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }


class WardUserRegisterForm(forms.ModelForm):
    """
    Form to register a new user
    """
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        strip=False,
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password again'}),
        strip=False,
    )

    ward = forms.ModelChoiceField(
        queryset=WardNumber.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='वार्ड नं छान्नुहोस् '
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'address',
            'contact_no',
            'designation',
            'email',
            'username',
            'password',
            'confirm_password',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        full_name = self.cleaned_data['full_name']

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password mismatch')
        if full_name.lower() in password.lower():
            raise forms.ValidationError('Password similar to name of user.')
        password_validation.validate_password(confirm_password, self.instance)
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
            raise forms.ValidationError('Invalid Email format')
        return email

    def save(self, commit=True):
        user = super(WardUserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # user.is_staff = True
        user.role = USER_ROLES.wardstaff
        user.is_confirmed = True
        if commit:
            user.save()
        # user.send_confirmation_email()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['designation'].empty_label = 'पद छान्नुहोस्'


class WardUserEditForm(forms.ModelForm):
    """
    Form to register a new user
    """

    ward = forms.ModelChoiceField(
        queryset=WardNumber.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='वार्ड नं छान्नुहोस् '
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'address',
            'contact_no',
            'designation',
            'email',
            'username',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
        }

    # def clean_confirm_password(self):
    #     password = self.cleaned_data['password']
    #     confirm_password = self.cleaned_data['confirm_password']
    #     full_name = self.cleaned_data['full_name']
    #
    #     if password and confirm_password and password != confirm_password:
    #         raise forms.ValidationError('Password mismatch')
    #     if full_name.lower() in password.lower():
    #         raise forms.ValidationError('Password similar to name of user.')
    #     password_validation.validate_password(confirm_password, self.instance)
    #     return confirm_password

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
            raise forms.ValidationError('Invalid Email format')
        return email

    def clean_contact_no(self):
        contact_no = self.cleaned_data['contact_no']
        if not re.match(r'\d{9,15}', contact_no):
            raise forms.ValidationError('Invalid phone number format.')

        return contact_no

    def save(self, commit=True):
        user = super(WardUserEditForm, self).save(commit=False)
        # user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        user.role = USER_ROLES.wardstaff
        user.is_confirmed = True
        if commit:
            user.save()
        # user.send_confirmation_email()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['designation'].empty_label = 'पद छान्नुहोस्'


class WardUserPasswordChangeForm(forms.Form):
    """
    Form to change user password
    """

    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password'}),
        strip=False,
    )

    confirm_new_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password password'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WardUserPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError('Password mismatch')
        password_validation.validate_password(confirm_new_password, self.user)
        return confirm_new_password

    def save(self, commit=True):
        password = self.cleaned_data["confirm_new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
