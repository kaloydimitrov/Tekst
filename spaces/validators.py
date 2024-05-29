from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_name_len(value):
    if len(value) < 2:
        raise ValidationError(
            _(f"Name can't be less than 2 characters ('{value}' is {len(value)})"),
            params={"value": value},
        )


def validate_description_len(value):
    if len(value) < 15:
        raise ValidationError(
            _(f"Description can't be less than 15 characters ('{value}' is {len(value)})"),
            params={"value": value},
        )
