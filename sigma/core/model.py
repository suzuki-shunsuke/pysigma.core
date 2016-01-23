from .error import ErrorContainer, UnitError
from .field import Field


class ModelMeta(type):
    def __new__(cls, classname, bases, namespace, **kwargs):
        fields = {}
        for key, field in namespace.items():
            if key.startswith("_"):
                continue
            if isinstance(field, Field):
                fields[key] = field
                field.__model_name__ = classname
                if not field._name:
                    field._name = key
        namespace["__fields__"] = fields
        return type.__new__(cls, classname, bases, namespace, **kwargs)


class Model(object, metaclass=ModelMeta):
    def __init__(self, *args, **kwargs):
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
        self.__init__(*args, **kwargs)
        return self
