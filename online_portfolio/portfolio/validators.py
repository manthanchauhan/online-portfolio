"""
validators for portfolio app
"""
from django.core.exceptions import ValidationError


def all_space_validator(name, raise_error=True):
    name = name.strip()

    if name == "":
        if raise_error:
            raise ValidationError
        else:
            return False

    return True
