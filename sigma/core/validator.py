"""
"""


class FieldValidator(object):
    """
    Attrs:
      validates: The list of validate functions.
    """
    def __init__(self):
        self.validates = []

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
