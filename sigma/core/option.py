"""
"""

from collections import OrderedDict
from functools import partial
from inspect import isclass

from .error import UnitError
from .util import _convert_camel_to_snake


class OptionMeta(type):
    """ The Meta Class of Option Class.
    """
    def __new__(cls, classname, bases, namespace, **kwargs):
        namespace.setdefault(
            "__option_name__", _convert_camel_to_snake(classname)
        )
        if "errors" in namespace:
            error_set = set()
            errors = namespace["errors"]
            if not isinstance(errors, dict):
                errors = {tuple(errors): UnitError}
                namespace["errors"] = errors
            for error in errors:
                if isinstance(error, Exception):
                    error_set.add(error)
                else:
                    error_set.update(error)
            namespace["error_tuple"] = tuple(error_set)
        return type.__new__(cls, classname, bases, namespace, **kwargs)


class Option(object, metaclass=OptionMeta):
    """
    Attrs:
      __option_name__: An Option name(str).
    """
    def __init__(self, *args):
        if len(args):
            self.value = args[0]
        else:
            if hasattr(self, "default"):
                self.value = self.default

    def __call__(self, field, value):
        if hasattr(self, "errors"):
            try:
                return self.validate(field, value)
            except self.error_tuple as e:
                for errors, Error in self.errors.items():
                    if isinstance(e, errors):
                        raise Error(self, value)
        else:
            return self.validate(field, value)

    def __get__(self, instance, owner):
        return partial(self.__call__, instance)


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
    def wrap(Option, name, validate_):
        def validate(self, field, value):
            return validate_(field, self, value)

        kwargs["__option_name__"] = (
            name if name else _convert_camel_to_snake(validate_.__name__)
        )
        kwargs["validate"] = validate
        return OptionMeta("Option", (Option,), kwargs)

    length = len(args)
    if not length:
        return partial(wrap, Option, False)
    elif length == 1:
        arg = args[0]
        if isinstance(arg, str):
            return partial(wrap, Option, arg)
        elif isclass(arg) and issubclass(arg, Option):
            return partial(wrap, arg, False)
        else:
            return wrap(Option, False, arg)
    elif length > 1:
        return partial(wrap, *args)
