import pytest

from sigma.core import Option, option, UnitError


class Size(Option):
    def validate(self, fleld, value):
        return value


def test_option():
    assert Size.__option_name__ == "size"
    size = Size("foo")
    assert size.value == "foo"
    assert size(None, 12) == 12


@option
def isodd(field, opt, value):
    if not value % 2:
        raise UnitError(opt, value)
    return value


@option(foo="bar", default=15)
def hello(field, opt, value):
    return value


@option(errors=(ValueError,))
def hello2(field, opt, value):
    raise ValueError()


def test_option2():
    isodd_ = isodd()
    assert isinstance(isodd_, Option)
    assert isodd.__option_name__ == "isodd"
    assert isodd_(None, 3) == 3
    with pytest.raises(UnitError):
        isodd_(None, 4)
    assert hello.foo == "bar"
    h = hello()
    assert isinstance(h, Option)
    assert h(None, 3) == 3
    assert h.value == 15
    h2 = hello2()
    with pytest.raises(UnitError):
        h2(None, 5)
