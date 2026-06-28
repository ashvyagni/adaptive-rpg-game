#!/bin/bash
# Adaptive RPG Battle - Universal Launcher
# Run this from anywhere - it finds the project automatically

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Set Qt platform for macOS
export QT_QPA_PLATFORM=cocoa

# Run the game
exec python3 main.py "$@"