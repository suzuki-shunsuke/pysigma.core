"""
"""

import re


def validate(Model, *args, **kwargs):
    return Model(*args, **kwargs)


def asdict(model):
    return dict((key, getattr(model, key)) for key in model.__fields__)


_u1 = re.compile(r'(.)([A-Z][a-z]+)')
_u2 = re.compile('([a-z0-9])([A-Z])')


def _convert_camel_to_snake(value):
    """
    """
    return _u2.sub(r'\1_\2', _u1.sub(r'\1_\2', value)).lower()
