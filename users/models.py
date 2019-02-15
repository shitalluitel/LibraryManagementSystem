from datetime import datetime, timedelta

import jwt
from django.contrib import auth

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, _user_has_module_perms, _user_has_perm
# from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import PermissionDenied
from django.db import models
from django.conf import settings
# from django.template.defaultfilters import safe
from django.utils.safestring import mark_safe
from .validators import UsernameValidator
# from django.core.mail import EmailMessage
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("User must have a valid email address.")

        if not kwargs.get('username'):
            raise ValueError('User must have a valid username')

        user = self.model(
            username=kwargs.get('username').strip(),
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)

        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model
    """
    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[UsernameValidator()],
        error_messages={
            'unique': 'User with this username already exists.',
        },
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'User with this email already exists.',
        },
    )
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    # is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        return super().save(*args, **kwargs)

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def generate_confirmation_token(self):
        payload = {
            'confirm': self.id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=7)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
        return token

    def send_confirmation_email(self):
        token = self.generate_confirmation_token()
        link = settings.BASE_URL + 'users/confirm_email?token={}'.format(token)
        html = '<html><body>Click on the below link to confirm your email.<br> <a href="{}">{}</a></body></html>'.format(
            link, link)
        # data = {
        #     'from': "{} <{}>".format('Daily Cost', settings.ADMIN_EMAIL),
        #     'to': self.email,
        #     'subject': "Email Confirmation",
        #     'html': html | safe
        # }

        # requests.post(settings.MAILGUN_SERVER,
        #               auth=("api", settings.MAILGUN_API_KEY),
        #               data=data)
        print('http://localhost:8000/users/confirm_email?token={}'.format(token))

        print('http://khaja.herokuapp.com/users/confirm_email?token={}'.format(token))

        # for gmail mail confirmation api
        # email = EmailMessage('subject: Email Confirmation ', html, to=[self.email])
        # email.content_subtype = "html"
        # # email.attach(html)
        # email.send()

    def generate_password_reset_token(self):
        payload = {
            'reset': self.id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=7)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
        return token

    def send_password_reset_email(self):
        token = self.generate_password_reset_token()
        link = settings.BASE_URL + 'users/password_reset?token={}'.format(token)
        # link = 'http://localhost' + '/users/password_reset?token={}'.format(token)
        html = '<html><body>Click on the below link to reset your password.<br> <a href="{}">{}</a></body></html>'.format(
            link, link)
        # data = {
        #     'from': "{} <{}>".format('Daily Cost', settings.ADMIN_EMAIL),
        #     'to': self.email,
        #     'subject': "Reset Password",
        #     'html': html
        # }

        # requests.post(settings.MAILGUN_SERVER,
        #               auth=("api", settings.MAILGUN_API_KEY),
        #               data=data)
        print('http://localhost:8000/users/password_reset?token={}'.format(token))

        print('http://khaja.herokuapp.com/users/password_reset?token={}'.format(token))
        # email = EmailMessage('subject: Reset Password ', html, to=[self.email])
        # email.content_subtype = "html"
        # # email.attach(html)
        # email.send()

    class Meta:
        db_table = "users"
        verbose_name = 'User'
        verbose_name_plural = 'users'
        permissions = (
            ('change_password', 'Can change password'),
        )


class Logs(models.Model):
    user = models.ForeignKey(User, related_name='logs', on_delete=models.DO_NOTHING)
    message = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_logs"
