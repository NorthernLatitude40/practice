# Installing VS Code Dev Containers Extension

## Manual Installation Instructions

Since the extension cannot be installed automatically in this environment, please follow these steps to install it manually:

### Method 1: Using VS Code GUI (Recommended)

1. **Open VS Code**
   - Launch Visual Studio Code on your local machine

2. **Open Extensions View**
   - Click on the Extensions icon in the Activity Bar (or press `Ctrl+Shift+X`)
   - Alternatively, go to View → Extensions

3. **Search for Remote - Containers**
   - In the search box, type: `Remote - Containers`
   - Look for the extension by Microsoft with ID `ms-vscode-remote.remote-containers`

4. **Install the Extension**
   - Click the "Install" button next to the Remote - Containers extension
   - Wait for the installation to complete (may require VS Code restart)

5. **Verify Installation**
   - The extension should appear in your installed extensions list
   - You'll see a green checkmark indicating it's active

### Method 2: Using Command Palette

1. Open VS Code
2. Press `Ctrl+Shift+P` to open the Command Palette
3. Type: `Extensions: Install Extensions` and press Enter
4. Search for `Remote - Containers`
5. Select it from the list and click Install

### Method 3: Using VS Code CLI (Alternative)

If you have VS Code installed on your local machine, run this command in your terminal:

```bash
code --install-extension ms-vscode-remote.remote-containers
```

## Required Dependencies

Before using Dev Containers, ensure you have:

1. **Docker** installed and running
   - Download from [https://www.docker.com/](https://www.docker.com/)
   - Verify with: `docker --version`

2. **VS Code** latest version
   - Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)

## Using the Dev Container

Once installed:

1. Open this project folder in VS Code
2. You should see a prompt: "Folder contains a Dev Container configuration file."
3. Click "Reopen in Container" or use the command palette (`Ctrl+Shift+P`) and select:
   `Remote-Containers: Reopen in Container`
4. The container will build automatically using the Dockerfile
5. Your development environment will be ready with all dependencies installed

## Troubleshooting

If you don't see the prompt:

- Click on the Remote indicator in the bottom-left corner (it shows "><" when connected to a remote)
- Select "Remote-Containers: Reopen in Container"

If Docker is not running:

- Start Docker Desktop from your applications menu
- The extension will show an error if Docker isn't available
