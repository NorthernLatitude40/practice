# Pytest Command-Line Options Exploration Summary

This document summarizes the exploration of various pytest command-line options and their effects on test output.

## Test Suite Overview

The auth_module project contains:
- **72 tests** across multiple test files
- Achieves **95% code coverage** across src/auth_module files
- Tests include: authentication, authorization, CRUD operations, security, models, and schemas

## Command-Line Options Explored

### Basic Test Run
```bash
pytest --cov=src/auth_module tests/ -v
```
- Shows test names and status (PASSED/FAILED)
- Displays code coverage summary
- Shows 26 deprecation warnings about datetime.utcnow() and Pydantic methods

### Short Traceback Format
```bash
pytest --cov=src/auth_module tests/ -v --tb=short
```
- Provides concise error tracebacks when tests fail
- Reduces verbosity of failure output compared to default

### Verbose Output
```bash
pytest --cov=src/auth_module tests/ -v --verbose
```
- Shows more detailed information about test collection
- Displays full module paths and function names
- Helps understand the test execution flow in detail

### Disable Warnings
```bash
pytest --cov=src/auth_module tests/ -v --disable-warnings
```
- Suppresses all warning messages (including deprecation warnings)
- Cleaner output when warnings are not relevant to current debugging

### Show Slowest Tests
```bash
pytest --cov=src/auth_module tests/ -v --durations=10
```
- Displays the 10 slowest test runs at the end
- Helps identify performance bottlenecks in the test suite
- Useful for optimizing test execution time

### Post-Mortem Debugging
```bash
pytest --cov=src/auth_module tests/ -v --pdb
```
- Enables Python debugger (PDB) on test failures
- Drops into interactive debugger when a test fails
- Allows inspection of variables and execution state
- Useful for debugging complex test failures

### Debug Logging
```bash
pytest --cov=src/auth_module tests/ -v --log-cli-level=DEBUG
```
- Shows debug-level log messages from the application
- Provides detailed insight into application behavior during tests
- Helps trace execution flow and identify issues

### Show Local Variables
```bash
pytest --cov=src/auth_module tests/ -v --showlocals
```
- Displays local variables when showing tracebacks
- Useful for understanding the state at failure points
- Complements --pdb by providing variable context without interactive debugging

## Combined Options

The most comprehensive command tested was:
```bash
pytest --cov=src/auth_module tests/ -v --tb=short --disable-warnings --durations=10 --pdb --log-cli-level=DEBUG --showlocals
```

This combination provides:
- Verbose test execution details
- Short, readable tracebacks
- No warning clutter
- Performance metrics for slow tests
- Interactive debugging on failures
- Detailed logging output
- Variable context in tracebacks

## Recommendations

### For Development
```bash
pytest --cov=src/auth_module tests/ -v --tb=short --disable-warnings
```
- Good balance of information and readability
- Suppresses irrelevant warnings
- Provides clear failure messages

### For Debugging
```bash
pytest --cov=src/auth_module tests/ -v --pdb --showlocals --log-cli-level=DEBUG
```
- Maximum debugging capability
- Interactive debugger on failures
- Full variable context and logging

### For Performance Analysis
```bash
pytest --cov=src/auth_module tests/ -v --durations=10
```
- Identifies slowest tests
- Helps optimize test suite performance

## Common Issues Encountered

### Deprecation Warnings
The test suite shows 26 deprecation warnings related to:
- `datetime.utcnow()` - Use `datetime.now(timezone.utc)` instead
- Pydantic's deprecated `.dict()` and `.json()` methods

These warnings are harmless but clutter the output. Using `--disable-warnings` provides cleaner output.

### Code Coverage
The project maintains excellent coverage (95%) across all source files in `src/auth_module`.

## Conclusion

Pytest offers extensive customization through command-line options. The right combination depends on the specific needs:
- **Quick checks**: Basic verbose mode with short tracebacks
- **Debugging**: Add PDB, show locals, and debug logging
- **Performance**: Add duration metrics
- **Clean output**: Disable warnings when appropriate

All tested combinations successfully ran 72 tests with consistent results.