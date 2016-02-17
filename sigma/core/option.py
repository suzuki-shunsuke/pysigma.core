"""
"""

from .util import _convert_camel_to_snake


class OptionMeta(type):
    """ The Meta Class of Option Class.
    """
    def __new__(cls, classname, bases, namespace, **kwargs):
        namespace.setdefault(
            "__option_name__", _convert_camel_to_snake(classname)
        )
        return type.__new__(cls, classname, bases, namespace, **kwargs)


class Option(object, metaclass=OptionMeta):
    """
    Attrs:
      __option_name__: An Option name(str).
    """
    def __init__(self, value):
        self.value = value

    def __call__(self, value):
        return self.validate(value)


def option(*args, **kwargs):
    """ Create An Option class.
    option(validate)
      validate: A callable object.
        validate function.

    option([Option,] [name,] **kwargs)
      Option: An Option class.
      name: An option name.
      **kwargs: Option class's attributes.

    Returns: An Option Class.
    """
    name = False

    def wrap(validate):
        kwargs["validate"] = validate
        kwargs["__option_name__"] = (
            name if name else _convert_camel_to_snake(validate.__name__)
        )
        return OptionMeta("Option", (Option,), kwargs)

    length = len(args)
    if length == 1:
        arg = args[0]
        if isinstance(arg, str):
            name = arg
            return wrap
        else:
            return wrap(arg)
    elif length > 1:
        name = args[0]
        validate = args[1]
        return wrap(validate)
    return wrap
