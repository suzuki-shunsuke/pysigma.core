from collections import OrderedDict
from inspect import isclass
from types import FunctionType

from .option import Option


class FieldMeta(type):
    """ The Meta Class of Field Class.
    """
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return OrderedDict()

    def __new__(cls, classname, bases, namespace, **kwargs):
        options = OrderedDict()
        for key, value in namespace.items():
            if isclass(value) and issubclass(value, Option):
                options[key] = value
        namespace["__Options__"] = options
        return type.__new__(cls, classname, bases, namespace, **kwargs)


class Field(object, metaclass=FieldMeta):
    """
    Attrs:
      __Options__: An OrderedDict instance.
        key: An option name.
        value: An Option class.
      __options__: An OrderedDict instance.
        key: An option name.
        value: An Option instance.
      __model_name__: A Model name.
      __field_name__: A Field name.
      __value__: A value.
    """
    def __init__(self, *args, **kwargs):
        """
        Args:
          *args:
            args[0]: A field name or list of option names or Option instances.
            args[1]: A list of option names or Option instances.
          *kwargs:
            key: An option name.
            value: An option's setting value.
        """
        length = len(args)
        _options = {}
        if not length:
            self.__field_name__ = ""
        elif length == 1:
            arg = args[0]
            if isinstance(arg, str):
                self.__field_name__ = arg
            else:
                for value in arg:
                    if isinstance(value, str):
                        _options[value] = self.__Options__[value]()
                    else:
                        _options[value.__option_name__] = value
                self.__field_name__ = ""
        else:
            self.__field_name__ = args[0]
            for value in arg:
                if isinstance(value, str):
                    _options[value] = self.__Options__[value]()
                else:
                    _options[value.__option_name__] = value
        for key, value in kwargs.items():
            _options[key] = self.__Options__[key](value)
        options = OrderedDict(
            (key, _options[key])
            for key in self.__Options__ if key in _options
        )
        self.__options__ = options
        self.__value__ = None
        self.__model_name__ = ""
        self.__model__ = None

    @property
    def value(self):
        return self.__value__

    @value.setter
    def value(self, value):
        self.__value__ = self.__validate__(value)

    def __get__(self, instance, owner):
        if instance:
            return instance.__data__[self.__field_name__]
        else:
            return self

    def __set__(self, instance, value):
        instance.__data__[self.__field_name__] = self.__validate__(value)

    def __validate__(self, value):
        for option in self.__options__.values():
            value = option(value)
        return value
