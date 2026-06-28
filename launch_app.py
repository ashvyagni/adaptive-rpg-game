#!/usr/bin/env python3
"""
Adaptive RPG Battle - macOS Launcher
This script ensures the correct Qt platform is set before importing PySide6
"""
import sys
import os

# MUST set this BEFORE importing PySide6
os.environ['QT_QPA_PLATFORM'] = 'cocoa'

# Also try to find Qt plugins if needed
if getattr(sys, 'frozen', False):
    # Running as compiled app
    qt_plugin_path = os.path.join(os.path.dirname(sys.executable), '..', 'PlugIns')
    if os.path.exists(qt_plugin_path):
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path

# Now import the actual game
from main import main

if __name__ == '__main__':
    main()
