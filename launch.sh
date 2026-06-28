#!/bin/bash
# Adaptive RPG Battle - Launcher

cd "$(dirname "$0")"

# Set Qt platform for macOS
export QT_QPA_PLATFORM=cocoa

# Run the game
python3 main.py