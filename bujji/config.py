"""
BUJJI AI — Configuration Module
================================
Centralizes all configuration: API keys, user preferences, paths, and defaults.
Loads from .env file and provides typed access to all settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Load environment variables from .env file (and fallback to .env.example if missing)
_env_path = PROJECT_ROOT / ".env"
_env_example_path = PROJECT_ROOT / ".env.example"

if _env_path.exists():
    load_dotenv(_env_path)

if not os.environ.get("GOOGLE_API_KEY") and _env_example_path.exists():
    load_dotenv(_env_example_path)

# ─── API Keys ────────────────────────────────────────────────────────────────

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# ─── Application Defaults ────────────────────────────────────────────────────

APP_NAME = "BUJJI AI"
APP_VERSION = "2.0.0"
APP_TAGLINE = "Your Intelligent Desktop Companion"

# Window dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WIDTH = 900
MIN_HEIGHT = 600
SIDEBAR_WIDTH = 240
SIDEBAR_COLLAPSED_WIDTH = 64

# ─── User Defaults ───────────────────────────────────────────────────────────

DEFAULT_USER_NAME = "Gouthami"
DEFAULT_PERSONALITY = "friendly"
DEFAULT_VOICE_INDEX = 1  # Female voice (index 1 in pyttsx3 SAPI5)
DEFAULT_VOICE_RATE = 175
DEFAULT_VOICE_VOLUME = 0.9
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"

# ─── Paths ────────────────────────────────────────────────────────────────────

DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "bujji.db"
ASSETS_DIR = PROJECT_ROOT / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
FONTS_DIR = ASSETS_DIR / "fonts"
SOUNDS_DIR = ASSETS_DIR / "sounds"
OUTPUT_DIR = PROJECT_ROOT / "output"
LEGACY_DIR = PROJECT_ROOT / "legacy"

# Ensure directories exist
for _dir in [DATA_DIR, ASSETS_DIR, ICONS_DIR, FONTS_DIR, SOUNDS_DIR, OUTPUT_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ─── Wake Words ───────────────────────────────────────────────────────────────

WAKE_WORDS = ["hey bujji", "hello bujji", "bujji", "wake up bujji", "are you there"]

# ─── Feature Flags ────────────────────────────────────────────────────────────

ENABLE_VOICE = True
ENABLE_WAKE_WORD = True
ENABLE_CONTINUOUS_LISTENING = False
ENABLE_NOTIFICATIONS = True
