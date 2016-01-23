"""
"""


def validate(Model, *args, **kwargs):
    return Model(*args, **kwargs)


def asdict(model):
    return dict((key, getattr(model, key)) for key in model.__fields__)
