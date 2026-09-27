# Development Container Setup

This directory contains configuration files for VS Code's Remote - Containers extension, which provides a consistent development environment.

## Features

- **Python 3.10** runtime with all project dependencies pre-installed
- **FastAPI** framework ready to use
- **Development tools**: Black (formatter), Pylint (linter), pytest (testing)
- **Port forwarding**: Ports 8000 and 8001 are forwarded for API development
- **Environment variables**: Pre-configured `.env` file for development

## Usage

### Prerequisites

1. Install [Docker](https://www.docker.com/)
2. Install [VS Code](https://code.visualstudio.com/)
3. Install the [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Starting the Development Container

1. Open this project folder in VS Code
2. When prompted, click "Reopen in Container" or use the command palette (Ctrl+Shift+P) and select "Remote-Containers: Reopen in Container"
3. The container will build automatically using the Dockerfile
4. Once built, you'll have a fully configured development environment

### Running the Application

Once inside the container:

```bash
# Run the FastAPI application
uvicorn src.auth_module.main:app --reload --host 0.0.0.0 --port 8000

# Or use the convenience script
./scripts/start_openhands.sh
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Configuration Files

- **`devcontainer.json`**: Main configuration for the development container
- **`Dockerfile`**: Docker image build instructions
- **`.env`**: Environment variables for development

## Customization

To customize the container:

1. Edit the files in this directory
2. Rebuild the container (Ctrl+Shift+P > "Remote-Containers: Rebuild Container")

## Troubleshooting

If you encounter issues:

- Check Docker is running (`docker ps`)
- Try rebuilding the container
- Check VS Code output for Remote-Containers logs
