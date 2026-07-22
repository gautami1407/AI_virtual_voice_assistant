"""
Landing Page — Home screen for BUJJI AI
==========================================
The first screen users see: animated logo, greeting, time/date,
weather mini-widget, recent chats, and quick action buttons.
"""

import datetime
import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, QUICK_ACTIONS
from bujji.ui.components.animated_logo import AnimatedLogo
from bujji.ui.components.glass_card import GlassCard
from bujji.ui.components.quick_actions import QuickActionsGrid


class LandingPage(ctk.CTkFrame):
    """
    Home/Landing page with:
    - Animated BUJJI logo
    - Time-based greeting
    - Live clock and date
    - Weather mini card
    - Recent conversations
    - Quick action buttons grid
    """

    def __init__(self, master, user_name="Gouthami", on_action=None, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)

        self._user_name = user_name
        self._on_action = on_action

        # Scrollable content
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["scrollbar_thumb"],
            scrollbar_button_hover_color=COLORS["border_light"],
        )
        self._scroll.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["lg"])

        # ─── Top Section: Logo + Greeting ─────────────────────────────────
        top = ctk.CTkFrame(self._scroll, fg_color="transparent")
        top.pack(fill="x", pady=(0, SPACING["xl"]))

        # Logo (left) and greeting (right) in a row
        top.columnconfigure(1, weight=1)

        # Animated Logo
        self._logo = AnimatedLogo(top, size=100)
        self._logo.grid(row=0, column=0, padx=(0, SPACING["xl"]), sticky="n")

        # Greeting & clock area
        greeting_frame = ctk.CTkFrame(top, fg_color="transparent")
        greeting_frame.grid(row=0, column=1, sticky="nw", pady=(SPACING["lg"], 0))

        # Greeting text
        greeting = self._get_greeting()
        self._greeting_label = ctk.CTkLabel(
            greeting_frame,
            text=f"{greeting}, {self._user_name}! 👋",
            font=("Segoe UI", 26, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        self._greeting_label.pack(fill="x")

        # Subtitle
        ctk.CTkLabel(
            greeting_frame,
            text="How can I help you today?",
            font=("Segoe UI", 14),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Date and Time
        self._datetime_label = ctk.CTkLabel(
            greeting_frame,
            text="",
            font=("Segoe UI", 13),
            text_color=COLORS["accent_cyan"],
            anchor="w",
        )
        self._datetime_label.pack(fill="x", pady=(12, 0))

        self._update_datetime()

        # ─── Status Cards Row ─────────────────────────────────────────────
        cards_row = ctk.CTkFrame(self._scroll, fg_color="transparent")
        cards_row.pack(fill="x", pady=(0, SPACING["xl"]))
        cards_row.columnconfigure((0, 1, 2), weight=1)

        # Weather mini card
        self._weather_card = GlassCard(cards_row, title="🌤  Weather")
        self._weather_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        self._weather_text = ctk.CTkLabel(
            self._weather_card.content,
            text="Click to check weather",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        self._weather_text.pack(fill="x")

        # System status mini card
        self._sys_card = GlassCard(cards_row, title="📊  System")
        self._sys_card.grid(row=0, column=1, padx=8, sticky="nsew")

        self._sys_text = ctk.CTkLabel(
            self._sys_card.content,
            text="Loading...",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        self._sys_text.pack(fill="x")

        # AI Status mini card
        self._ai_card = GlassCard(cards_row, title="🤖  AI Status")
        self._ai_card.grid(row=0, column=2, padx=(8, 0), sticky="nsew")

        self._ai_text = ctk.CTkLabel(
            self._ai_card.content,
            text="Gemini 2.0 Flash\n● Ready",
            font=("Segoe UI", 12),
            text_color=COLORS["success"],
            anchor="w",
        )
        self._ai_text.pack(fill="x")

        # ─── Quick Actions ────────────────────────────────────────────────
        ctk.CTkLabel(
            self._scroll,
            text="Quick Actions",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(0, SPACING["md"]))

        self._quick_actions = QuickActionsGrid(
            self._scroll,
            actions=QUICK_ACTIONS,
            columns=4,
            on_action=self._handle_action,
        )
        self._quick_actions.pack(fill="x", pady=(0, SPACING["xl"]))

        # ─── Recent Conversations ─────────────────────────────────────────
        ctk.CTkLabel(
            self._scroll,
            text="Recent Conversations",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(0, SPACING["md"]))

        self._recent_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self._recent_frame.pack(fill="x", pady=(0, SPACING["xl"]))

        # Placeholder for empty state
        self._empty_label = ctk.CTkLabel(
            self._recent_frame,
            text="No recent conversations yet.\nStart chatting with BUJJI! 💬",
            font=("Segoe UI", 13),
            text_color=COLORS["text_tertiary"],
            justify="center",
        )
        self._empty_label.pack(pady=SPACING["xl"])

        # Load system status
        self._update_system_status()

    def _get_greeting(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            return "Good Morning"
        elif hour < 17:
            return "Good Afternoon"
        else:
            return "Good Evening"

    def _update_datetime(self):
        """Update the live clock."""
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        self._datetime_label.configure(text=f"📅 {date_str}  •  🕐 {time_str}")
        self.after(1000, self._update_datetime)

    def _update_system_status(self):
        """Fetch and display basic system info."""
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=0)
            mem = psutil.virtual_memory().percent
            battery = psutil.sensors_battery()
            bat_str = f"{battery.percent}%" if battery else "N/A"
            self._sys_text.configure(
                text=f"CPU: {cpu}%\nRAM: {mem}%\nBattery: {bat_str}"
            )
        except Exception:
            self._sys_text.configure(text="Unable to read")
        self.after(5000, self._update_system_status)

    def _handle_action(self, action_key):
        if self._on_action:
            self._on_action(action_key)

    def update_recent_conversations(self, conversations):
        """Update the recent conversations list."""
        # Clear existing
        for widget in self._recent_frame.winfo_children():
            widget.destroy()

        if not conversations:
            self._empty_label = ctk.CTkLabel(
                self._recent_frame,
                text="No recent conversations yet.\nStart chatting with BUJJI! 💬",
                font=("Segoe UI", 13),
                text_color=COLORS["text_tertiary"],
                justify="center",
            )
            self._empty_label.pack(pady=SPACING["xl"])
            return

        for conv in conversations[:5]:
            card = GlassCard(self._recent_frame)
            card.pack(fill="x", pady=4)

            ctk.CTkLabel(
                card.content,
                text=conv.get("title", "Untitled Chat"),
                font=("Segoe UI", 13, "bold"),
                text_color=COLORS["text_primary"],
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                card.content,
                text=conv.get("preview", ""),
                font=("Segoe UI", 11),
                text_color=COLORS["text_secondary"],
                anchor="w",
            ).pack(fill="x")

    def update_weather(self, weather_text):
        """Update the weather mini card text."""
        self._weather_text.configure(text=weather_text)
