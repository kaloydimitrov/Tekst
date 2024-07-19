from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags


def validate_name_len(value):
    if len(value) < 2:
        raise ValidationError(
            _(f"Name can't be less than 2 characters ('{value}' is {len(value)})"),
            params={"value": value},
        )


def validate_description_len(value):
    if len(strip_tags(value)) < 15:
        raise ValidationError(
            _(f"Description can't be less than 15 characters ('{value}' is {len(strip_tags(value))})"),
            params={"value": value},
        )
