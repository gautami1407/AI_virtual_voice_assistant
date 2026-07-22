"""
BUJJI AI — Design System & Theme
=================================
Color palette, typography, spacing, and design tokens for the entire application.
Dark theme with deep black, navy, purple accent, and neon cyan.
"""

# ─── Color Palette ────────────────────────────────────────────────────────────

COLORS = {
    # Backgrounds
    "bg_primary":       "#0A0E1A",   # Deepest black-blue (main bg)
    "bg_secondary":     "#111827",   # Slightly lighter (panel bg)
    "bg_tertiary":      "#1A1F35",   # Card hover state
    "bg_card":          "#1E293B",   # Glassmorphism card surface
    "bg_card_hover":    "#243348",   # Card hover
    "bg_input":         "#0F172A",   # Input field background
    "bg_sidebar":       "#0D1322",   # Sidebar background
    "bg_sidebar_hover": "#1A2540",   # Sidebar item hover
    "bg_sidebar_active":"#1E3A5F",   # Sidebar active item

    # Accent Colors
    "accent_purple":    "#8B5CF6",   # Primary accent (buttons, links)
    "accent_purple_hover": "#7C3AED",
    "accent_cyan":      "#06B6D4",   # Secondary accent
    "accent_neon":      "#00F5D4",   # Neon green (highlights, active states)
    "accent_blue":      "#3B82F6",   # Info blue
    "accent_pink":      "#EC4899",   # Pink for special elements

    # Text
    "text_primary":     "#F1F5F9",   # Main text (white-ish)
    "text_secondary":   "#94A3B8",   # Muted text
    "text_tertiary":    "#64748B",   # Very muted text
    "text_accent":      "#A78BFA",   # Purple-tinted text
    "text_on_accent":   "#FFFFFF",   # Text on accent backgrounds

    # Borders
    "border":           "#1E293B",   # Subtle borders
    "border_light":     "#334155",   # Slightly visible borders
    "border_accent":    "#8B5CF680", # Purple border with transparency

    # Status Colors
    "success":          "#10B981",   # Green
    "warning":          "#F59E0B",   # Amber
    "error":            "#EF4444",   # Red
    "info":             "#3B82F6",   # Blue

    # Chat
    "chat_user_bg":     "#312E81",   # User message bubble
    "chat_ai_bg":       "#1E293B",   # AI message bubble
    "chat_user_text":   "#E0E7FF",
    "chat_ai_text":     "#E2E8F0",

    # Gradients (start, end)
    "gradient_purple":  ("#8B5CF6", "#6D28D9"),
    "gradient_cyan":    ("#06B6D4", "#0891B2"),
    "gradient_mixed":   ("#8B5CF6", "#06B6D4"),
    "gradient_neon":    ("#00F5D4", "#06B6D4"),

    # Scrollbar
    "scrollbar_bg":     "#111827",
    "scrollbar_thumb":  "#334155",

    # Waveform
    "waveform_active":  "#8B5CF6",
    "waveform_idle":    "#334155",
    "waveform_glow":    "#A78BFA",
}

# ─── Typography ───────────────────────────────────────────────────────────────

FONTS = {
    # Font families (CustomTkinter uses system fonts)
    "family_primary":   "Segoe UI",       # Main UI font
    "family_heading":   "Segoe UI",       # Headings
    "family_mono":      "Cascadia Code",  # Code/monospace
    "family_display":   "Segoe UI Black", # Large display text (logo)

    # Font sizes
    "size_xs":          11,
    "size_sm":          12,
    "size_base":        13,
    "size_md":          14,
    "size_lg":          16,
    "size_xl":          20,
    "size_2xl":         24,
    "size_3xl":         32,
    "size_4xl":         40,
    "size_display":     48,
}

# Pre-built font tuples for CTk widgets
def font(size_key="size_base", weight="normal", family_key="family_primary"):
    """Create a font tuple for CustomTkinter widgets."""
    family = FONTS[family_key]
    size = FONTS[size_key]
    return (family, size, weight)


FONT_BODY = font("size_base")
FONT_BODY_BOLD = font("size_base", "bold")
FONT_SMALL = font("size_sm")
FONT_SMALL_BOLD = font("size_sm", "bold")
FONT_CAPTION = font("size_xs")
FONT_HEADING = font("size_xl", "bold")
FONT_SUBHEADING = font("size_lg", "bold")
FONT_TITLE = font("size_2xl", "bold", "family_heading")
FONT_DISPLAY = font("size_3xl", "bold", "family_display")
FONT_HERO = font("size_display", "bold", "family_display")
FONT_MONO = font("size_sm", "normal", "family_mono")
FONT_MONO_BOLD = font("size_sm", "bold", "family_mono")
FONT_SIDEBAR = font("size_base")
FONT_SIDEBAR_ACTIVE = font("size_base", "bold")

# ─── Spacing ──────────────────────────────────────────────────────────────────

SPACING = {
    "xs":   4,
    "sm":   8,
    "md":   12,
    "lg":   16,
    "xl":   20,
    "2xl":  24,
    "3xl":  32,
    "4xl":  40,
    "5xl":  48,
}

# ─── Border Radius ────────────────────────────────────────────────────────────

RADIUS = {
    "sm":   6,
    "md":   8,
    "lg":   12,
    "xl":   16,
    "2xl":  20,
    "full": 9999,
}

# ─── Shadows (for canvas-based glassmorphism) ─────────────────────────────────

SHADOWS = {
    "sm":   {"offset": 2,  "blur": 4,  "color": "#00000040"},
    "md":   {"offset": 4,  "blur": 8,  "color": "#00000060"},
    "lg":   {"offset": 8,  "blur": 16, "color": "#00000080"},
    "glow": {"offset": 0,  "blur": 20, "color": "#8B5CF640"},
}

# ─── Animation Durations (ms) ─────────────────────────────────────────────────

ANIMATION = {
    "fast":     100,
    "normal":   200,
    "slow":     400,
    "pulse":    1500,    # Logo pulse cycle
    "typing":   80,      # Typing indicator dot cycle
    "waveform": 50,      # Waveform update interval
    "fade":     300,     # Page transition fade
}

# ─── Sidebar Config ───────────────────────────────────────────────────────────

SIDEBAR_ITEMS = [
    {"key": "home",        "icon": "🏠", "label": "Home"},
    {"key": "voice",       "icon": "🎤", "label": "Voice Chat"},
    {"key": "chat",        "icon": "💬", "label": "AI Chat"},
    {"key": "tools",       "icon": "⚡",  "label": "Productivity"},
    {"key": "developer",   "icon": "💻", "label": "Developer Hub"},
    {"key": "files",       "icon": "📁", "label": "Files"},
    {"key": "weather",     "icon": "🌤", "label": "Weather"},
    {"key": "news",        "icon": "📰", "label": "News"},
    {"key": "reminders",   "icon": "🗓", "label": "Reminders"},
    {"key": "camera",      "icon": "📷", "label": "Camera"},
    {"key": "games",       "icon": "🎮", "label": "Games"},
    {"key": "settings",    "icon": "⚙",  "label": "Settings"},
    {"key": "monitor",     "icon": "📊", "label": "System Monitor"},
]

# ─── Quick Actions for Landing Page ──────────────────────────────────────────

QUICK_ACTIONS = [
    {"icon": "🎤", "label": "Voice Chat",     "action": "voice"},
    {"icon": "💬", "label": "Ask BUJJI",       "action": "chat"},
    {"icon": "⚡", "label": "Tools & AI",     "action": "tools"},
    {"icon": "💻", "label": "Developer",      "action": "developer"},
    {"icon": "🌤", "label": "Weather",         "action": "weather"},
    {"icon": "📰", "label": "News",            "action": "news"},
    {"icon": "📊", "label": "System Status",   "action": "monitor"},
    {"icon": "⚙",  "label": "Settings",        "action": "settings"},
]
