import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def phone_no_validation(value):
    regx = re.compile(r'^\d{6}$|\d{3}-\d{6}$|\d{2}-\d{7}$|\d{3}-\d{10}$|\d{10}$')
    if not regx.match(value):
        raise ValidationError(_(
            "Must be one of the following:- xxx-xxxxxx, xxxxxx, xx-xxxxxxx,\
             xxx-xxxxxxxxxx, xxxxxxxxxx"))
