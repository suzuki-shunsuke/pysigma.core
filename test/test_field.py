from sigma.core import Field

import pytest


def test_value():
    field = Field()
    assert field.value is None
    field.value = 1
    assert field.value == 1


def test_attr():
    class User(object):
        name = Field()
    assert User.name is None
    User.name = 5
    assert User.name == 5
