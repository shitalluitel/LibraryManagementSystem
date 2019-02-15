from django.core.exceptions import PermissionDenied


def is_customer(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 1 or request.user.is_admin:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
