from django.core.exceptions import ValidationError

def non_empty(val):
    if not val.strip():
        raise ValidationError("Can't be empty")
