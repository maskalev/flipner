from django.core.exceptions import ValidationError


def validate_price(price):
    if not 0 < price < 100_000:
        raise ValidationError("Price must be more than 0 and less than 100 000")
