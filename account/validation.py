import re

from rest_framework.exceptions import ValidationError


def validate_mobile_number(value):
    if re.compile(r"\d{10}").match(value):
        return value
    else:
        raise ValidationError("Phone number entered is incorrect.")


def validate_email(email):
    if len(email) > 6:
        if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) != None:
            return email
        else:
            raise ValidationError("Email entered is Incorrect.")
    raise ValidationError("Email is Incorrect")
