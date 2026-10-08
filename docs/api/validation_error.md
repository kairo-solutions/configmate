# ValidationError Exception

Raised when configuration validation fails.

## API Reference

For the full API, see the [source code](../../../configmate/config.py).

## Example

```python
from configmate import Config, ValidationError

config = Config()
config.validate('port', lambda x: 0 < x < 65536)  # port must be in valid range
config.set('port', 70000)  # invalid port

try:
    config.validate_all()
except ValidationError as e:
    print(f"Validation error: {e}")
```