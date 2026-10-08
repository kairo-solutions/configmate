# Contributing to ConfigMate

Thank you for considering contributing to ConfigMate! We welcome contributions from the community.

## How to Contribute

### Reporting Issues
- Use the [GitHub issue tracker](https://github.com/kairo-solutions/configmate/issues/new/choose)
  to report bugs or suggest features
- Please include as much detail as possible, including:
  - Steps to reproduce the issue
  - Expected vs actual behavior
  - Your environment (Python version, OS, etc.)
  - Relevant code snippets or error messages

### Preparing Issues for Drips Wave

ConfigMate can be proposed to a Drips Wave program by its maintainers. Follow
the [Drips Wave maintainer process](https://docs.drips.network/wave/): apply the
repository to a program and wait for approval before listing work for a Wave.
Once approved, choose work that can be completed and reviewed within the cycle.

For each candidate issue, describe the problem and why it matters, a bounded
scope and exclusions, observable acceptance criteria and tests, and relevant
code areas or dependencies. Avoid broad requests or tasks whose completion
depends on unbounded design work. Maintain the issue and be available for
questions and pull request review during the cycle. Add point values through
the active Wave program's process rather than guessing them in an issue.

### Pull Requests
1. Fork the repository
2. Create a new branch for your feature or fix
3. Make your changes
4. Add or update tests as needed
5. Ensure all tests pass
6. Submit a pull request with a clear description of your changes

## Development Setup

### Prerequisites
- Python 3.7+
- git

### Installation for Development
```bash
# Clone the repository
git clone https://github.com/kairo-solutions/configmate.git
cd configmate

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov
```

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=configmate

# Run a specific test file
pytest tests/test_config.py
```

## Code Style
- Follow PEP 8 for Python code style
- Use descriptive variable and function names
- Write clear, concise docstrings for public functions and classes
- Add type hints where possible
- Keep lines to a maximum of 88 characters when possible

## Commit Messages
- Use clear, descriptive commit messages
- Follow the convention: "type: description"
- Types include: feat, fix, docs, style, refactor, test, chore
- Examples:
  - `feat: add nested configuration support`
  - `fix: correct type conversion for boolean values`
  - `docs: update README with usage examples`
  - `test: add tests for environment variable loading`

## License
By contributing to ConfigMate, you agree that your contributions will be licensed under the MIT License.

## Getting Help
If you need help with your contribution, please:
- Check the existing documentation
- Look at similar contributions in the project's history
- Ask for clarification in the issue tracker

Thank you for helping make ConfigMate better!
