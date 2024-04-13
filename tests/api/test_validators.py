import pytest
from django.core.exceptions import ValidationError

from api.validators import validate_price


class TestValidatePrice:
    def test_price_less_than_1(self):
        with pytest.raises(ValidationError):
            validate_price(0)

    def test_price_more_than_99_999(self):
        with pytest.raises(ValidationError):
            validate_price(100_000)

    def test_valid_price(self):
        try:
            validate_price(42)
        except ValidationError:
            pytest.fail("validate_price raised ValidationError unexpectedly")
