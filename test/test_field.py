from sigma.core import Field

import pytest


class Type(object):
    __option_name__ = "type"

    def __init__(self, type_):
        self.type = type_

    def __call__(self, field, value):
        return self.type(value)


def test_value():
    field = Field(Type(int))
    assert field.value is None
    field.value = 1
    assert field.value == 1
    with pytest.raises(ValueError):
        field.value = "foo"
