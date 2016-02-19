from sigma.core import Field, Model, option, UnitError, ErrorContainer

import pytest


class FooError(UnitError):
    pass


class NameField(Field):
    @option
    def error(self, option, value):
        raise FooError(option, value)


class User(Model):
    name = NameField()
    password = NameField(error=None)


def test_model():
    user = User()
    user.name = "foo"
    assert user.name == "foo"
    user = user(name="bar")
    assert isinstance(user, User)
    assert user.name == "bar"
    user = User(name="zoo")
    assert user.name == "zoo"


def test_unit_error():
    user = User()
    with pytest.raises(FooError):
        user.password = None


def test_unit_error2():
    with pytest.raises(FooError):
        User(True, password=None)


def test_error_container():
    with pytest.raises(ErrorContainer):
        User(password=None)


def test_error_container2():
    with pytest.raises(ErrorContainer):
        User(False, password=None)
