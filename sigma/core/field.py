from collections import OrderedDict
from inspect import isclass

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
            args[0]: A field name or list of option names.
            args[1]: A list of option names.
          *kwargs:
            key: An option name.
            value: An option's setting value.
        """
        length = len(args)
        self.__field_name__ = ""
        static_option_names = set()
        if length == 1:
            arg = args[0]
            if isinstance(arg, str):
                self.__field_name__ = arg
            else:
                static_option_names = set(arg)
        elif length > 1:
            self.__field_name__ = args[0]
            static_option_names = set(args[1])
        options = OrderedDict()
        for name, ops in self.__Options__.items():
            if name in static_option_names:
                o = ops()
                options[name] = o
                setattr(self, name, o)
            elif name in kwargs:
                o = ops(kwargs[name])
                options[name] = o
                setattr(self, name, o)
            elif getattr(ops, "omit", False):
                o = ops()
                options[name] = o
                setattr(self, name, o)
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
            value = option(self, value)
        return value
