"""
BUJJI AI — Desktop Application Entry Point
===========================================
Main executable script for BUJJI AI Desktop Assistant.
"""

import sys
import os

# Add project root directory to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from bujji.app import BujjiApp

def main():
    """Launch BUJJI AI Application."""
    app = BujjiApp()
    app.run()

if __name__ == "__main__":
    main()