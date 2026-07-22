# Smart Talk - AI Virtual Voice Assistant

A cross-platform Python desktop application for voice commands and AI assistance.

## Setup

1. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Environment Variables

The following environment variables are required for full functionality:

| Variable | Description |
|----------|-------------|
| `HF_TOKEN` | Hugging Face API token (for AI features) |
| `WEATHER_API_KEY` | OpenWeatherMap API key (for weather commands) |
| `GOOGLE_API_KEY` | Google Generative AI API key (for AI chat features) |

## Asset Management

This application uses a centralized asset management system (`assets.py`) for portable file paths.

### Changes Made

All hardcoded absolute file paths have been replaced with a portable solution:

- **Before**: `C:\Users\N.SIRISHA\OneDrive\Pictures\Documents\bujji.jpg`
- **After**: Uses `assets.get_gif_path("bujji.gif")` to find assets relative to project root

### How It Works

1. **Asset Loading**: All assets are loaded from the project root directory (`AI-virtual-voice-assistant/`)
2. **Fallback Support**: If an asset is missing, a warning is shown and a placeholder is displayed
3. **Cross-Platform**: Uses `pathlib.Path` for compatibility with Windows, Linux, and macOS
4. **Output Files**: Screenshots and camera pictures are saved to the project root directory

### Required Assets

Place the following files in the project root or `assets/` subdirectory:
- `bujji.gif` - Animated GIF for the assistant display

## Security Improvements

All hardcoded API keys and tokens have been removed from the source code:

- **Before**: Hardcoded tokens in `main.py` and `features.py`
- **After**: Tokens loaded from environment variables via `os.environ.get()`

### Files Changed for Security

| File | Change |
|------|--------|
| `main.py` | Removed `WEATHER_API_KEY` and `HF_TOKEN`, now uses `os.environ.get()` |
| `features.py` | Removed `GOOGLE_API_KEY`, now uses `os.environ.get()` |
| `.env.example` | Added template for environment variables |
| `.gitignore` | Added `.env` to prevent accidental commits |

## Git Commands to Remove Secrets from History

If secrets exist in previous Git commits, run these commands to remove them:

```bash
# Remove secrets from all commits (use with caution!)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all

# Or use the modern BFG Repo-Cleaner tool:
# java -jar bfg.jar --replace-text secrets.txt

# Force push (will overwrite remote history - coordinate with team!)
git push origin --force --all
git push origin --force --tags
```

## File Structure

```
AI-virtual-voice-assistant/
├── main.py           # Main application entry point
├── features.py       # Voice assistant features
├── functions.py      # Core functions (speech recognition, TTS)
├── gui.py            # GUI components
├── assets.py         # Asset path management
├── game_hub.py       # Mini games
├── bujji.gif          # Assistant animation
├── .env.example      # Environment variable template
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Requirements

- Python 3.7+
- tkinter
- PIL/Pillow
- opencv-python
- pyautogui
- psutil
- speechrecognition
- pyttsx3
- google-generativeai
- requests
- wikipedia
- beautifulsoup4
- spotipy