from collections import OrderedDict


class Field(object):
    """
    Attrs:
      __options__: An OrderedDict instance.
        key: An option name.
        value: An Option instance.
      __model_name__: A Model name.
      __field_name__: A Field name.
      __value__: A value.
    """
    def __init__(self, *args, **kwargs):
        """
        Field([name,] [option, ...])
        Args:
          name: A Field name.
          *args: A list of Option instances.
        """
        self.kwargs = kwargs
        length = len(args)
        self.__field_name__ = ""
        self.__options__ = OrderedDict()
        if args:
            arg = args[0]
            if isinstance(args, str):
                self.__field_name__ = arg
                args = args[1:]
            self.__options__ = OrderedDict(
                (opt.__option_name__, opt) for opt in args
            )
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
        for opt in self.__options__.values():
            value = opt(self, value)
        return value
