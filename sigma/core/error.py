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
      option: An option instance.
      value: A value tried to set.
      model_name: A Model name.
      field_name: A Field name.
    """
    def __init__(self, option, value):
        """
        Args:
          option: An option instance.
          value: A value tried to set.
        """
        self.option = option
        self.value = value
        field = getattr(option, "field", False)
        self.field_name = field.__field_name__ if field else ""
        self.model_name = field.__model_name__ if field else ""
        super(UnitError, self).__init__()

    def __str__(self):
        return ("{}!\n"
                "Model: {}\n"
                "Field: {}\n"
                "option: {}\n"
                "value: {}").format(
            self.__class__.__name__,
            self.model_name,
            self.field_name,
            self.option.__option_name__,
            self.value
        )
