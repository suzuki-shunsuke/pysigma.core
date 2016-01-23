# sigma.core

sigma.core is a validation framework.

## Example

```python
from sigma.core import Model, ErrorContainer, asdict, validate
from sigma.standard import Field


class User(Model):
    id = Field(type=int, size=(5, 10))
    password = Field(type=str, length=(8, 15))

user = User()
user.id = 5
user.password = "12345678"
asdict(user)  # {"id": 5, "password": "12345678"}
```

```python
user.id = 20  # raise OverMaxError
```

```python
user.password = 10  # raise InvalidTypeError
```

```python
try:
    user = User(id=20, password=10)
except ErrorContainer as errors:
    errors["id"]  # OverMaxError
    errors["password"]  # InvalidTypeError
```

> ##### Note
> The above *type*, *size* and *length* validation functions and error classes are not included in sigma.core packages.  
> They are included in sigma.standard packages.

```python
user = User(id=20, password=10)  # raise ErrorContainer
# equivalent to
# user = User(False, id=20, password=10)
```

```python
user = User(True, id=20, password=10)  # raise OverMaxError or InvalidTypeError
```

```python
validate(User, *args, **kwargs)
```

is equivalent to

```python
User(*args, **kwargs)
```

If you merely want to validate values and don't need the return value(Model instance),  
use *validate* function to make the meaning clear.


## Install

```
$ pip install sigma.core
```

## Dependencies

* Nothing

## License

sigma is available under the [MIT License](http://opensource.org/licenses/mit-license.php).
