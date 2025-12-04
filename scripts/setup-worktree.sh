#!/bin/bash

set -e

WORKTREE_PATH="${1:-$(pwd)}"

echo "Setting up worktree at: $WORKTREE_PATH"
cd "$WORKTREE_PATH"

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    
    PYTHON_CMD=""
    for version in 3.14 3.13 3.12 3.11 3.10; do
        if command -v "python${version}" >/dev/null 2>&1; then
            PYTHON_CMD="python${version}"
            break
        fi
    done

    if [ -z "$PYTHON_CMD" ]; then
        if command -v python3 >/dev/null 2>&1; then
            PYTHON_CMD="python3"
        else
            echo "Warning: No Python 3 installation found"
            echo "Skipping virtual environment setup"
            exit 0
        fi
    fi

    echo "Using $PYTHON_CMD for virtual environment"
    "$PYTHON_CMD" -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    pip install --upgrade pip
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    
    echo "✓ Virtual environment created and dependencies installed"
else
    echo "Virtual environment already exists at .venv"
fi

if [ -f "package.json" ]; then
    echo "Installing npm dependencies..."
    npm install
    echo "✓ npm dependencies installed"
fi

# If the repo provides a setup-filesystem script in the scripts directory (same repo), run it
SCRIPTS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/

if [ -f "${SCRIPTS_DIR}setup-filesystem.sh" ]; then
    echo "Setting up filesystem..."
    if bash "${SCRIPTS_DIR}setup-filesystem.sh"; then
        echo "✓ Filesystem setup completed"
    else
        echo "⚠ Filesystem setup failed (environment variables may not be configured)"
        echo "  You can run '${SCRIPTS_DIR}setup-filesystem.sh' manually after configuring environment variables"
    fi
fi
