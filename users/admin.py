# from django.contrib import admin
#
# # Register your models here.
#
# fields = ['image_tag']
# readonly_fields = ['image_tag']
#
# from .models import User
#
# admin.site.register(User)

from django import forms
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from users.models import User, Logs

admin.site.register(User)
# admin.site.unregister(Group)
admin.site.register(Logs)