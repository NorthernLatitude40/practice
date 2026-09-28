#!/bin/bash
set -e

echo "Setting up remote container environment (simple approach)..."

# Create cache directory if it doesn't exist
mkdir -p /tmp/vscode-server-cache

# Check if VS Code Server is already downloaded and extracted
if [ ! -d "/tmp/vscode-server-cache/vscode-server-linux-x64" ]; then
    echo "Downloading VS Code Server..."
    wget https://update.code.visualstudio.com/commit:04c0d99f4fb0d8afe6ce4f0c58e31e183ac3e4b1/server-linux-x64/stable -O /tmp/vscode-server-cache/vscode-server-linux-x64.tar.gz
    echo "Extracting VS Code Server..."
    tar -xzf /tmp/vscode-server-cache/vscode-server-linux-x64.tar.gz -C /tmp/vscode-server-cache/
fi

# Set environment variables for remote containers
echo "Setting up environment variables..."
export VSCODE_REMOTE_CONTAINERS=1
export VSCODE_REMOTE_SERVER_PATH=/tmp/vscode-server-cache/vscode-server-linux-x64/bin/code-server

# Add to bashrc for persistence
cat >> ~/.bashrc << 'EOF'
# VS Code Remote Containers support
export VSCODE_REMOTE_CONTAINERS=1
export VSCODE_REMOTE_SERVER_PATH=/tmp/vscode-server-cache/vscode-server-linux-x64/bin/code-server
EOF

# Source the environment variables
source ~/.bashrc

# Verify VS Code Server is available
echo "Verifying VS Code Server installation..."
if [ -f "/tmp/vscode-server-cache/vscode-server-linux-x64/bin/code-server" ]; then
    echo "VS Code Server successfully installed at: /tmp/vscode-server-cache/vscode-server-linux-x64/bin/code-server"
    echo "Environment variables set:"
    echo "  VSCODE_REMOTE_CONTAINERS=$VSCODE_REMOTE_CONTAINERS"
    echo "  VSCODE_REMOTE_SERVER_PATH=$VSCODE_REMOTE_SERVER_PATH"
else
    echo "Error: VS Code Server not found at expected location"
    exit 1
fi

echo "Remote container setup complete!"
echo "You can now try to reopen the project in a remote container."
