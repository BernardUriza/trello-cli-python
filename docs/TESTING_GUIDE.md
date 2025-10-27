# Testing Guide - Trello CLI

## Overview

This guide covers testing strategies, pytest setup, and continuous integration for the Trello CLI project.

## Prerequisites

```bash
pip install pytest pytest-cov pytest-mock
```

## Project Structure for Tests

```
trello-cli-python/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_validators.py       # Current tests
│   ├── test_commands/           # Command tests
│   │   ├── test_board.py
│   │   ├── test_list.py
│   │   ├── test_card.py
│   │   ├── test_bulk.py
│   │   ├── test_sprint.py
│   │   ├── test_query.py
│   │   └── test_standardize.py
│   ├── test_integration/        # Integration tests
│   │   └── test_workflows.py
│   └── fixtures/                # Test data
│       ├── boards.json
│       ├── cards.json
│       └── sample.csv
```

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_validators.py
```

### Run with Coverage
```bash
pytest --cov=trello_cli --cov-report=html tests/
```

### Run with Verbose Output
```bash
pytest -v tests/
```

### Run Tests Matching Pattern
```bash
pytest -k "test_bulk" tests/
```

## Writing Tests

### Example: Testing Validators

```python
"""
tests/test_validators.py
"""
import pytest
from datetime import datetime
from trello_cli.utils.validators import validate_date, validate_color

def test_validate_date_valid():
    """Test valid date formats"""
    result = validate_date("2025-12-25")
    assert isinstance(result, datetime)
    assert result.year == 2025
    assert result.month == 12
    assert result.day == 25

def test_validate_date_invalid():
    """Test invalid date format"""
    with pytest.raises(ValueError):
        validate_date("invalid-date")

def test_validate_color_valid():
    """Test valid colors"""
    assert validate_color("red") == True
    assert validate_color("blue") == True

def test_validate_color_invalid():
    """Test invalid color"""
    with pytest.raises(ValueError):
        validate_color("invalid")
```

### Example: Testing Commands with Mocks

```python
"""
tests/test_commands/test_board.py
"""
import pytest
from unittest.mock import Mock, patch
from trello_cli.commands.board import cmd_boards

@patch('trello_cli.commands.board.get_client')
def test_cmd_boards(mock_get_client):
    """Test boards command"""
    # Setup mock
    mock_client = Mock()
    mock_board = Mock()
    mock_board.id = "board123"
    mock_board.name = "Test Board"
    mock_client.list_boards.return_value = [mock_board]
    mock_get_client.return_value = mock_client

    # Run command (capture output)
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output

    cmd_boards()

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    # Assertions
    assert "Test Board" in output
    assert "board123" in output
    mock_client.list_boards.assert_called_once()
```

### Example: Testing Bulk Operations

```python
"""
tests/test_commands/test_bulk.py
"""
import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from trello_cli.commands.bulk import cmd_bulk_create_cards

@patch('trello_cli.commands.bulk.get_client')
def test_bulk_create_cards_csv(mock_get_client, tmp_path):
    """Test bulk card creation from CSV"""
    # Create temporary CSV file
    csv_content = """title,description,due_date,labels
Card 1,Description 1,2025-12-25,red:P0
Card 2,Description 2,2025-12-30,blue:Feature"""

    csv_file = tmp_path / "cards.csv"
    csv_file.write_text(csv_content)

    # Setup mocks
    mock_client = Mock()
    mock_list = Mock()
    mock_list.add_card = Mock(return_value=Mock(id="card123"))
    mock_client.get_list.return_value = mock_list
    mock_get_client.return_value = mock_client

    # Run command
    cmd_bulk_create_cards("list123", str(csv_file))

    # Assertions
    assert mock_list.add_card.call_count == 2
```

### Example: Testing Sprint Commands

```python
"""
tests/test_commands/test_sprint.py
"""
import pytest
from unittest.mock import Mock, patch
from trello_cli.commands.sprint import cmd_sprint_status

@patch('trello_cli.commands.sprint.get_client')
def test_sprint_status(mock_get_client):
    """Test sprint status command"""
    # Setup mocks
    mock_client = Mock()
    mock_board = Mock()
    mock_board.name = "Test Board"

    # Create mock lists
    mock_ready = Mock()
    mock_ready.name = "✅ Ready"
    mock_ready.closed = False
    mock_ready.list_cards.return_value = [Mock(labels=[]) for _ in range(5)]

    mock_in_progress = Mock()
    mock_in_progress.name = "⚙️ In Progress"
    mock_in_progress.closed = False
    mock_in_progress.list_cards.return_value = [Mock(labels=[]) for _ in range(3)]

    mock_board.list_lists.return_value = [mock_ready, mock_in_progress]
    mock_client.get_board.return_value = mock_board
    mock_get_client.return_value = mock_client

    # Run command
    cmd_sprint_status("board123")

    # Verify calls
    mock_board.list_lists.assert_called_once()
```

## Fixtures

### conftest.py - Shared Fixtures

```python
"""
tests/conftest.py
"""
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_trello_client():
    """Mock Trello client for testing"""
    client = Mock()
    client.list_boards = Mock(return_value=[])
    client.get_board = Mock()
    client.get_list = Mock()
    client.get_card = Mock()
    return client

@pytest.fixture
def mock_board():
    """Mock Trello board"""
    board = Mock()
    board.id = "board123"
    board.name = "Test Board"
    board.url = "https://trello.com/b/test"
    board.list_lists = Mock(return_value=[])
    board.add_list = Mock()
    return board

@pytest.fixture
def mock_list():
    """Mock Trello list"""
    lst = Mock()
    lst.id = "list123"
    lst.name = "Test List"
    lst.closed = False
    lst.list_cards = Mock(return_value=[])
    lst.add_card = Mock()
    return lst

@pytest.fixture
def mock_card():
    """Mock Trello card"""
    card = Mock()
    card.id = "card123"
    card.name = "Test Card"
    card.desc = "Test Description"
    card.due = None
    card.labels = []
    card.url = "https://trello.com/c/test"
    return card

@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a sample CSV file for testing"""
    csv_content = """title,description,due_date,labels
Test Card 1,Description 1,2025-12-25,red:P0
Test Card 2,Description 2,,blue:Feature"""

    csv_file = tmp_path / "test_cards.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)

@pytest.fixture
def sample_json_file(tmp_path):
    """Create a sample JSON file for testing"""
    import json

    data = [
        {"title": "Card 1", "description": "Desc 1", "due_date": "2025-12-25", "labels": ["red:P0"]},
        {"title": "Card 2", "description": "Desc 2", "due_date": "", "labels": ["blue:Feature"]}
    ]

    json_file = tmp_path / "test_cards.json"
    json_file.write_text(json.dumps(data))
    return str(json_file)
```

## Integration Tests

### Testing Complete Workflows

```python
"""
tests/test_integration/test_workflows.py
"""
import pytest
from unittest.mock import Mock, patch

class TestSprintWorkflow:
    """Test complete sprint workflow"""

    @patch('trello_cli.commands.sprint.get_client')
    def test_complete_sprint_cycle(self, mock_get_client):
        """Test start -> status -> close workflow"""
        # Setup
        mock_client = self._setup_sprint_board()
        mock_get_client.return_value = mock_client

        # 1. Start sprint
        # 2. Check status
        # 3. Close sprint

        # Assertions
        pass

    def _setup_sprint_board(self):
        """Helper to create sprint board mock"""
        client = Mock()
        # Setup complete board structure
        return client
```

## Coverage Goals

- **Minimum Coverage**: 70%
- **Target Coverage**: 85%
- **Critical Paths**: 95%

### Generate Coverage Report

```bash
pytest --cov=trello_cli --cov-report=html --cov-report=term tests/
```

View HTML report:
```bash
open htmlcov/index.html
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-mock

    - name: Run tests with coverage
      run: |
        pytest --cov=trello_cli --cov-report=xml tests/

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Best Practices

### 1. Test Naming Convention
- Use descriptive names: `test_<feature>_<scenario>`
- Example: `test_bulk_move_cards_with_filter`

### 2. Arrange-Act-Assert Pattern
```python
def test_example():
    # Arrange
    mock_data = create_test_data()

    # Act
    result = function_under_test(mock_data)

    # Assert
    assert result == expected_value
```

### 3. Mock External Dependencies
- Always mock Trello API calls
- Mock file system operations
- Mock user input

### 4. Test Edge Cases
- Empty inputs
- Invalid data
- API failures
- Network timeouts

### 5. Parametrized Tests
```python
@pytest.mark.parametrize("color,expected", [
    ("red", True),
    ("blue", True),
    ("invalid", False),
])
def test_validate_color(color, expected):
    result = validate_color(color)
    assert result == expected
```

## Testing Checklist

- [ ] Unit tests for all commands
- [ ] Integration tests for workflows
- [ ] Mock all external API calls
- [ ] Test error handling
- [ ] Test edge cases
- [ ] Achieve >70% coverage
- [ ] CI/CD pipeline configured
- [ ] Coverage reports generated

## Troubleshooting

### Issue: Import Errors
```python
# Add project root to Python path in conftest.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### Issue: Mock Not Working
```python
# Use full path in patch decorator
@patch('trello_cli.commands.board.get_client')  # ✅ Full path
# not
@patch('get_client')  # ❌ Relative path
```

### Issue: Fixtures Not Found
```python
# Ensure conftest.py is in correct location
tests/
  conftest.py  # ✅ Here for all tests
  test_something.py
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Python unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)

## Next Steps

1. Implement unit tests for new commands
2. Add integration tests for complete workflows
3. Configure CI/CD pipeline
4. Set up code coverage tracking
5. Add pre-commit hooks for running tests
