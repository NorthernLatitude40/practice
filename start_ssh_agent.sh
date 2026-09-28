#!/bin/bash
# Start SSH agent and verify it's working

eval "$(ssh-agent)" && (ssh-add -l || true) || echo "Failed to start SSH agent"
