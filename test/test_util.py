from sigma.core import Field, Model, asdict

import pytest


class User(Model):
    name = Field()
    password = Field()


def test_asdict():
    user = User(name="foo", password="bar")
    assert asdict(user) == {"name": "foo", "password": "bar"}
    user2 = User(name="foo")
    assert asdict(user2) == {"name": "foo", "password": None}
