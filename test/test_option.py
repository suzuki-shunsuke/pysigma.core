import pytest

from sigma.core import Option, option, UnitError


class Size(Option):
    pass


def test_option():
    @option
    def isodd(option, value):
        if not value % 2:
            raise UnitError()
        return value
