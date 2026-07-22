"""
BUJJI AI — Module Main Entry Point
Allows running: python -m bujji
"""

import sys
import os

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from bujji.app import BujjiApp

def main():
    app = BujjiApp()
    app.run()

if __name__ == "__main__":
    main()
