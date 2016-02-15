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
    def __call__(self, value):
        pass


def option(*args, **kwargs):
    """
    Args:
      *args:
        arg[0]: A callable object or option name(str).
        arg[1]: A callable object.
      *kwargs: Option Class's attributes.
    Returns: An Option Class.
    """
    name = False

    def wrap(func):
        kwargs["__call__"] = func
        kwargs["__option_name__"] = (
            name if name else _convert_camel_to_snake(func.__name__)
        )
        return type("Option", (Option,), kwargs)

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
        func = args[1]
        return wrap(func)
    return wrap
