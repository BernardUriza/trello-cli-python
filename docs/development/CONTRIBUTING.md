# Contributing to Trello CLI Python

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/bernardurizaorozco/trello-cli-python.git
cd trello-cli-python
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
pip3 install pytest  # For testing
```

### 3. Configure Trello API

```bash
./trello config
```

## Project Structure

```
trello-cli-python/
├── trello_cli/          # Main package
│   ├── commands/        # Command modules
│   │   ├── board.py
│   │   ├── list.py
│   │   ├── card.py
│   │   └── label.py
│   ├── utils/           # Utility modules
│   │   ├── formatters.py
│   │   └── validators.py
│   ├── cli.py           # CLI entry point
│   ├── client.py        # Trello API wrapper
│   └── config.py        # Configuration management
├── tests/               # Test suite
├── examples/            # Usage examples
└── trello               # Main executable
```

## Code Style

- Follow PEP 8 guidelines
- Use docstrings for all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

## Adding New Commands

### 1. Create Command Module

Create a new file in `trello_cli/commands/`:

```python
# trello_cli/commands/my_command.py
"""
My command description
"""

from ..client import get_client

def cmd_my_command(arg1, arg2):
    """Execute my command"""
    client = get_client()
    # Implementation here
    print("✅ Command executed successfully")
```

### 2. Register Command

Add to `trello_cli/commands/__init__.py`:

```python
from .my_command import cmd_my_command

__all__ = [..., 'cmd_my_command']
```

### 3. Add CLI Handler

Add to `trello_cli/cli.py` in the `main()` function:

```python
elif command == 'my-command':
    if len(sys.argv) < 3:
        print("❌ Usage: trello my-command <arg1> <arg2>")
        sys.exit(1)
    cmd_my_command(sys.argv[2], sys.argv[3])
```

### 4. Update Documentation

Add command to `HELP_TEXT` in `cli.py` and `README.md`.

### 5. Add Tests

Create test file in `tests/test_my_command.py`:

```python
"""
Tests for my_command
"""

def test_my_command():
    # Test implementation
    pass
```

## Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_validators.py

# Run with coverage
python3 -m pytest --cov=trello_cli tests/
```

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update README.md if needed

3. **Test Your Changes**
   ```bash
   python3 -m pytest tests/
   ./trello --help  # Verify CLI works
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/my-feature
   ```
   Then create a Pull Request on GitHub.

## Commit Message Guidelines

Use clear, descriptive commit messages:

- ✨ `feat: Add support for card attachments`
- 🐛 `fix: Handle empty board lists gracefully`
- 📚 `docs: Update README with new examples`
- ♻️ `refactor: Simplify date validation logic`
- ✅ `test: Add tests for label commands`
- 🎨 `style: Format code with black`

## Code Review

All submissions require review. We'll:
- Check code quality and style
- Verify tests pass
- Ensure documentation is updated
- Test functionality manually

## Questions?

Feel free to:
- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Contact the maintainer directly

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
