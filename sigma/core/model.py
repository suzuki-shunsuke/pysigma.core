from .error import ErrorContainer, UnitError
from .field import Field


class ModelMeta(type):
    """ A Model Meta Class.
    """
    def __new__(cls, classname, bases, namespace, **kwargs):
        fields = {}
        result = type.__new__(cls, classname, bases, namespace, **kwargs)
        for key, field in namespace.items():
            if key.startswith("_"):
                continue
            if isinstance(field, Field):
                fields[key] = field
                field.__Model__ = result
                field.__model__ = None
                field.__model_name__ = classname
                if not field._name:
                    field._name = key
        result.__fields__ = fields
        return result


class Model(object, metaclass=ModelMeta):
    """
    Attrs:
      __fields__: A list of Field instances.
    """
    def __init__(self, *args, **kwargs):
        """
        Args:
          *args:
            arg[0]: True or False.
          **kwargs:
            key: An option name.
            value: An option's setting value.
        """
        self.__values__ = dict((key, None) for key in self.__fields__)
        for key, field in self.__fields__.items():
            field.__model__ = self
        if args and args[0]:
            for key, value in kwargs.items():
                setattr(self, key, value)
        else:
            errors = ErrorContainer()
            for key, value in kwargs.items():
                try:
                    setattr(self, key, value)
                except UnitError as e:
                    errors[key] = e
            if errors:
                raise errors

    def __call__(self, *args, **kwargs):
        """
        Args:
          Equal to __init__ constructor.
        Returns:
          self
        """
        self.__init__(*args, **kwargs)
        return self
