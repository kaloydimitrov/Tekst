from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_len(value):
    if len(value) < 3:
        raise ValidationError(
            _(f"Can't be less than 3 characters ('{value}' is {len(value)})"),
            params={"value": value},
        )
