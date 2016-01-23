"""
"""

from collections import UserDict


class SigmaError(Exception):
    """Generic Error Class.
    All sigma's error classes are this subclasses.
    """
    pass


class ErrorContainer(UserDict, SigmaError):
    """ Contain multiple errors.

    key: A field name.
    value: A SigmaError instance.

    Example:
      from sigma.core import Model, ErrorContainer
      from sigma.standard import Field

      class User(Model):
          id = Field(type=int)
          name = Field(length=(3, None))

      try:
          user = User(id="foo", name="12")
      except ErrorContainer as errors:
          for key, error in errors.items():
              print(key, type(error))
              # id, InvalidTypeError
              # name, TooShortError
    """
    def __init__(self, **kwargs):
        """
        """
        UserDict.__init__(self, **kwargs)

    def __str__(self):
        return "The following Errors have raised!\n\n{}".format(
            "\n\n".join("{}\n{}".format(key, val) for key, val in self.items())
        )


class UnitError(SigmaError):
    """
    Attributes:
      field: A Field instance.
      option: A option instance.
      value: A value tried to set.
      model_name: A Model name.
    """
    def __init__(self, field, option, value):
        """
        Args:
          field: A Field instance.
          option: A option instance.
          value: A value tried to set.
        """
        self.field = field
        self.option = option
        self.value = value
        self.model_name = field.__model_name__
        super(UnitError, self).__init__()

    def __str__(self):
        return ("{}!\n"
                "Model: {}\n"
                "Field: {}\n"
                "option: {}\n"
                "value: {}").format(
            self.__class__.__name__,
            self.model_name,
            self.field._name,
            self.option.name,
            self.value
        )
