"""
"""

from functools import partial


class FieldValidator(object):
    """
    """
    def __init__(self, field, *args, **kwargs):
        """
        Args:
          field: A Field instance.
          *args: A list of validate function names.
          **kwargs: Keyword arguments of the Field constructor.
            key: An option name
            value: An option setting value.
        """
        self.field = field
        self.args = args
        self.kwargs = kwargs
        validates = []
        for key in field.__order__:
            option = field.__options__[key]
            if key in kwargs:
                option.value = kwargs[key]
                validates.append(
                    partial(option.func, field, option)
                )
            elif hasattr(option, "default"):
                option.value = option.default
                validates.append(
                    partial(option.func, field, option)
                )
            elif option.required or key in args:
                validates.append(partial(option.func, field, option))
        self.validates = validates

    def validate(self, value):
        """ Validate value.
        Args:
          value:
        Returns:
          A validated value.
        Raises:
          UnitError
        """
        for validate in self.validates:
            value = validate(value)
        return value
