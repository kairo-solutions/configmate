# ValidationError Exception

Raised when configuration validation fails.

## API Reference

For the full API, see the [source code](https://github.com/kairo-solutions/configmate/blob/master/configmate/config.py).

## Example

```python
from configmate import Config

config = Config()
config.validate('port', lambda x: 0 < x < 65536)  # port must be in valid range
config.set('port', 70000)  # invalid port

errors = config.validate_all()
if errors:
    print("\n".join(errors))
```