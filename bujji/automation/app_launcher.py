"""
App Launcher — Application Shortcuts & Management
==================================================
Launches desktop applications like Notepad, VS Code, File Explorer, Chrome, Camera, etc.
"""

import os
import sys
import subprocess


APP_MAP = {
    "notepad": "notepad.exe",
    "vscode": "code",
    "code": "code",
    "chrome": "chrome",
    "calc": "calc.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "explorer": "explorer.exe",
}


def open_app(app_name):
    """Open desktop application by name."""
    name_clean = app_name.lower().strip()
    cmd = APP_MAP.get(name_clean, name_clean)

    try:
        if sys.platform == "win32":
            os.system(f"start {cmd}")
        else:
            subprocess.Popen([cmd])
        return f"Opening {app_name}..."
    except Exception as e:
        return f"Could not launch {app_name}: {e}"


def open_file_explorer(path=None):
    """Open Windows File Explorer at user home or given path."""
    target_path = path or os.path.expanduser("~")
    try:
        if sys.platform == "win32":
            os.startfile(target_path)
        else:
            subprocess.Popen(["xdg-open", target_path])
        return f"Opening File Explorer at {target_path}"
    except Exception as e:
        return f"Failed to open File Explorer: {e}"
