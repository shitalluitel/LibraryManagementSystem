from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.safestring import mark_safe

from .validators import UsernameValidator
from model_utils import Choices


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

        user.role = 'admin'
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        # user.is_confirmed = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    """
    User model
    """

    objects = UserManager()

    # REQUIRED_FIELDS = ['username']

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def is_superuser(self):
        return self.is_active == True and self.is_superuser == True

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

        # email = EmailMessage('subject: Reset Password ', html, to=[self.email])
        # email.content_subtype = "html"
        # # email.attach(html)
        # email.send()

    class Meta:
        db_table = "users"


class Logs(models.Model):
    user = models.ForeignKey(User, related_name='logs', on_delete=models.DO_NOTHING)
    message = models.TextField(max_length=256)
    table = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_logs"
