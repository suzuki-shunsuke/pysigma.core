from collections import OrderedDict
from functools import partial
from types import FunctionType

from .validator import FieldValidator


class option(object):
    def __init__(self, **kwargs):
        self.name = ""
        self.kwargs = kwargs
        self.required = kwargs.get("required", False)
        self.value = None
        if "default" in kwargs:
            self.default = kwargs["default"]

    def __call__(self, name, func):
        self.name = name
        self.func = func
        return self


class FieldMeta(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return OrderedDict()

    def __new__(cls, classname, bases, namespace, **kwargs):
        options = {}
        for key, func in namespace.items():
            if key.startswith("_"):
                continue
            if isinstance(func, option):
                options[key] = func
            if isinstance(func, FunctionType):
                options[key] = option()(key, func)
        namespace["__options__"] = options
        namespace.setdefault("__order__", list(options.keys()))
        return type.__new__(cls, classname, bases, namespace, **kwargs)


class Field(object, metaclass=FieldMeta):
    __Validator__ = FieldValidator

    def __init__(self, *args, **kwargs):
        self._name = args[0] if args else ""
        self.__kwargs__ = kwargs
        self._value = None
        self.__model_name__ = ""
        validates = []
        for key in self.__order__:
            option = self.__options__[key]
            if key in kwargs:
                option.value = kwargs[key]
                validates.append(
                    partial(option.func, self, option)
                )
            elif hasattr(option, "default"):
                option.value = option.default
                validates.append(
                    partial(option.func, self, option)
                )
            elif option.required:
                validates.append(partial(option.func, self, option))
        self.__validator__ = self.__Validator__()
        self.__validator__.validates = validates

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = self.__validator__.validate(val)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value
