#!/bin/bash
set -e

echo "Setting up remote container environment..."

# Create cache directory if it doesn't exist
mkdir -p /tmp/vscode-server-cache

# Check if VS Code Server is already downloaded and extracted
if [ ! -d "/tmp/vscode-server-cache/vscode-server-linux-x64" ]; then
    echo "Downloading VS Code Server..."
    wget https://update.code.visualstudio.com/commit:04c0d99f4fb0d8afe6ce4f0c58e31e183ac3e4b1/server-linux-x64/stable -O /tmp/vscode-server-cache/vscode-server-linux-x64.tar.gz
    echo "Extracting VS Code Server..."
    tar -xzf /tmp/vscode-server-cache/vscode-server-linux-x64.tar.gz -C /tmp/vscode-server-cache/
fi

# Create symlink to make it easier to reference
echo "Creating symlink for VS Code Server..."
sudo ln -sf /tmp/vscode-server-cache/vscode-server-linux-x64 /usr/local/vscode-server || true

# Set environment variables for remote containers
echo "Setting up environment variables..."
cat >> /etc/profile.d/vscode-remote.sh << 'EOF'
export VSCODE_REMOTE_CONTAINERS=1
export VSCODE_REMOTE_SERVER_PATH=/usr/local/vscode-server/bin/code-server
EOF

# Make the script executable
sudo chmod +x /etc/profile.d/vscode-remote.sh

# Source the environment variables
source /etc/profile.d/vscode-remote.sh

# Verify VS Code Server is available
echo "Verifying VS Code Server installation..."
if [ -f "/usr/local/vscode-server/bin/code-server" ]; then
    echo "VS Code Server successfully installed at: /usr/local/vscode-server/bin/code-server"
else
    echo "Warning: VS Code Server not found at expected location"
fi

echo "Remote container setup complete!"
