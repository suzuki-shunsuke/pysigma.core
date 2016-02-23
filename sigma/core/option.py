"""
"""


class Option(object):
    """
    Attrs:
      __option_name__: An Option name(str).
      def __call__(self, field, value):
    """
    __option_name__ = __name__
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
