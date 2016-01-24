from collections import OrderedDict
from types import FunctionType

from .validator import FieldValidator


class option(object):
    """
    Attrs:
      name: The option name (Default is "").
      func: The validation function.
      kwargs: The keyword arguments of the constructor.
      required: Whether this option is required (Default is False).
      value: The option's setting value (Default is None).
      default(option):
        The option's default setting value.
        This attribute is created when "default" keyword argument
        is passed to the constructor.
    """
    def __init__(self, **kwargs):
        """
        Args:
          **kwargs:
            required: Whether this option is required (Default is False).
            default: The option's default setting value.
        """
        self.name = ""
        self.kwargs = kwargs
        self.required = kwargs.get("required", False)
        self.value = None
        if "default" in kwargs:
            self.default = kwargs["default"]

    def __call__(self, func):
        """
        Args:
          name: The option name.
          func: The validation function.
        Returns:
          self
        """
        self.name = func.__name__
        self.func = func
        return self


class FieldMeta(type):
    """ The Meta Class of Field Class.
    Attrs:
    """
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
                options[key] = option()(func)
        namespace["__options__"] = options
        namespace.setdefault("__order__", list(options.keys()))
        return type.__new__(cls, classname, bases, namespace, **kwargs)


class Field(object, metaclass=FieldMeta):
    """
    Attrs:
      __order__:
        The list of option names.
        Validation functions is executed in order of this list.
      __options__: The list of option instances.
      __Validator__:
        A FieldValidator class.
      __validator__:
        A __Validator__ instance.
      __model_name__: A Model name.
    """
    __Validator__ = FieldValidator

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
        validate_names = []
        if not length:
            self._name = ""
        elif length == 1:
            arg = args[0]
            if isinstance(arg, str):
                self._name = arg
            else:
                validate_names = arg
                self._name = ""
        else:
            self._name = args[0]
            validate_names = args[1]
        self.__args__ = args
        self.__kwargs__ = kwargs
        self._value = None
        self.__model_name__ = ""
        self.__model__ = None
        self.__validator__ = self.__Validator__(
            self, *validate_names, **kwargs
        )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = self.__validator__.validate(val)

    def __get__(self, instance, owner):
        if instance:
            return instance.__values__[self._name]
        else:
            return self

    def __set__(self, instance, value):
        instance.__values__[self._name] = self.__validator__.validate(value)
