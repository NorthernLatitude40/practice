#!/bin/bash
# Start SSH agent and verify it's working

# Start the SSH agent and export environment variables
eval "$(ssh-agent)"

# Verify the agent is working
if [ -n "$SSH_AUTH_SOCK" ] && [ -n "$SSH_AGENT_PID" ]; then
    echo "SSH agent started successfully"
    echo "Agent PID: $SSH_AGENT_PID"
    echo "Authentication socket: $SSH_AUTH_SOCK"
    ssh-add -l || echo "The agent has no identities."
else
    echo "Failed to start SSH agent"
fi
