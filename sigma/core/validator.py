"""
"""


class FieldValidator(object):
    def __init__(self):
        self.validates = []

    def validate(self, value):
        for validate in self.validates:
            value = validate(value)
        return value
