from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser():
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Not Authorised ')
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def wardstaff_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_wardstaff():
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Not Authorised ')
            return HttpResponseRedirect('/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
