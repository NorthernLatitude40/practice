# Testing and Coverage Guide

This guide explains how to run unit tests and view coverage in this project.

## Prerequisites

- Python 3.10+
- pip (Python package manager)
- pytest (included in requirements.txt)
- pytest-cov (for coverage reporting)

## Running Tests

### Basic Test Execution

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/unit/test_crud.py
```

Run specific test method:

```bash
pytest tests/unit/test_crud.py::TestCRUDOperations::test_get_user_by_email_exists
```

### Running Tests with Coverage

The project is configured to run coverage automatically. Use these commands:

**Terminal output (text):**

```bash
pytest --cov=src/auth_module --cov-report=term-missing
```

This will show you which lines are not covered in the terminal.

**HTML report:**

```bash
pytest --cov=src/auth_module --cov-report=html
```

After running this, open `htmlcov/index.html` in your browser to see an interactive coverage report.

**XML report (for CI/CD):**

```bash
pytest --cov=src/auth_module --cov-report=xml
```

Generates a `coverage.xml` file for integration with CI tools like GitHub Actions, Jenkins, etc.

## VSCode Coverage Visualization

### Prerequisites

1. Install the Python extension in VSCode
2. Install the "Coverage Gutters" extension (recommended)

### Using VSCode Test Explorer

1. Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P)
2. Search for "Testing: Run All Tests"
3. Select it to run all tests with coverage

The test results will appear in the Testing sidebar.

### Viewing Coverage in VSCode

After running tests, you can view coverage:

1. **Coverage Gutters**: Install the "Coverage Gutters" extension
   - Green lines = covered code
   - Red lines = uncovered code
   - Yellow lines = partially covered

2. **Coverage Report View**:
   - Open the Testing sidebar (Ctrl+Shift+T or Cmd+Shift+T)
   - Click on "Coverage" tab to see detailed coverage statistics

## Coverage Configuration

The coverage configuration is in `pytest.ini`:

```ini
[pytest]
pythonpath = src
testpaths = tests
addopts = --cov=src/auth_module --cov-report=term-missing --cov-report=html --cov-report=xml
```

This configures:

- `--cov=src/auth_module`: Measure coverage of the auth_module package
- `--cov-report=term-missing`: Show missing lines in terminal
- `--cov-report=html`: Generate HTML report in htmlcov/ directory
- `--cov-report=xml`: Generate XML report for CI tools

## Interpreting Coverage Results

### Terminal Output Example

```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/auth_module/crud.py     100     20    80%   45-47, 60-65
src/auth_module/models.py    50      5    90%   30, 45
-------------------------------------------------------
TOTAL                      150     25    83%
```

### HTML Report Features

The HTML report provides:

- File-by-file breakdown
- Line-by-line coverage visualization
- Clickable navigation between files
- Summary statistics

## Best Practices for Writing Testable Code

1. **Keep functions small and focused** - Easier to test individual behaviors
2. **Dependency injection** - Pass dependencies as parameters rather than creating them internally
3. **Avoid global state** - Use fixtures or mocks for external resources
4. **Test edge cases** - Not just happy paths
5. **Keep tests isolated** - Each test should be independent
6. **Use meaningful test names** - Describe what the test is verifying

## Common Issues and Solutions

### Issue: Coverage shows 0%

**Solution:** Make sure you're running pytest with the --cov flag, or use the configured pytest.ini settings.

### Issue: Some lines not covered but should be

**Solution:** Check if those lines are in `__init__.py` files or other module-level code that may not be executed during tests. Consider adding explicit import tests if needed.

### Issue: Coverage report not generated

**Solution:** Ensure pytest-cov is installed (`pip install pytest-cov`). Check that the coverage configuration in pytest.ini is correct.

## CI/CD Integration

For GitHub Actions, add this to your workflow:

```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=src/auth_module --cov-report=xml

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```
