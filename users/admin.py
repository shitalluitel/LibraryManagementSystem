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


from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_admin')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
