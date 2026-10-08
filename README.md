# ConfigMate

A simple, powerful configuration management library for Python applications.

## Features

- Load configuration from multiple sources (environment variables, files, defaults)
- Automatic type conversion and validation
- Nested configuration support
- Easy to use API
- Zero dependencies

## About Kairo Solutions

ConfigMate is maintained by Kairo Solutions, a technology organization focused on building reliable, developer-friendly open source tools. Our mission is to simplify complex development challenges through well-designed, intuitive libraries that integrate seamlessly into modern Python workflows.

We believe in:
- **Simplicity without sacrifice**: Powerful features that don't complicate the developer experience
- **Reliability**: Thoroughly tested, stable releases you can depend on in production
- **Community-driven development**: Transparent processes that welcome contributions from developers worldwide
- **Practical solutions**: Tools designed to solve real-world problems faced by Python developers daily

## Installation

```bash
pip install configmate
```

## Usage

```python
from configmate import Config

config = Config()
config.load_from_env(prefix='APP_')
config.load_from_file('config.yaml')
config.set_default('debug', False, bool)

debug = config.get('debug')
database_url = config.get('database.url')
```

## License

MIT
