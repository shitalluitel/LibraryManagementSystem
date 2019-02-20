import django

from settings.models import Setting

if django.VERSION >= (1, 10, 0):
    MIDDLEWARE_MIXIN = django.utils.deprecation.MiddlewareMixin
else:
    MIDDLEWARE_MIXIN = object


class SettingCustomeMiddleware(MIDDLEWARE_MIXIN):
    def process_request(self, request):
        request.fine_amount = Setting.get_fine_amount()
        request.renew_days = Setting.get_renew_days()
        request.books_allowed = Setting.get_books_allowed()
