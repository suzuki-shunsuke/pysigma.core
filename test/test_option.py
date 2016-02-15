import pytest

from sigma.core import Option, option, UnitError


class Size(Option):
    pass


def test_option():
    @option
    def isodd(option, value):
        if not value % 2:
            raise UnitError()

    assert option.value is None
    option.value = 1
    assert option.value == 1
