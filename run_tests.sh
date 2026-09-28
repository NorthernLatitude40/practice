#!/bin/bash
# Simple script to run tests with coverage

echo "Running unit tests with coverage..."
pytest --cov=src/auth_module --cov-report=term-missing --cov-report=html --cov-report=xml -v

echo ""
echo "Coverage report generated in htmlcov/ directory"
echo "Open htmlcov/index.html in your browser to view the interactive report"
