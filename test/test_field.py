from sigma.core import Field

import pytest


def test_value():
    field = Field()
    assert field.value is None
    field.value = 1
    assert field.value == 1
