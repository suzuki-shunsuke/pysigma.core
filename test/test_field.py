from sigma.core import Field, option

import pytest


class Integer(Field):
    @option(omit=True)
    def type(self, opt, value):
        return int(value)


def test_value():
    field = Field()
    assert field.value is None
    field.value = 1
    assert field.value == 1
    a = Integer()
    a.value = 1
    assert a.value == 1
    with pytest.raises(ValueError):
        a.value = "foo"
