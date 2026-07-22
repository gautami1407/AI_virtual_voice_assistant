"""
Settings Page — User Preferences, Voice & API Configuration
============================================================
Configure user name, AI personality mode, Gemini API keys, TTS voice settings.
"""

import customtkinter as ctk
from bujji.config import DEFAULT_USER_NAME, GOOGLE_API_KEY
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard


class SettingsPage(ctk.CTkFrame):
    """
    Settings & Preferences view page.
    """

    def __init__(self, master, app_controller=None, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)
        self.app = app_controller

        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["scrollbar_thumb"],
        )
        self._scroll.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["lg"])

        # Header
        header = ctk.CTkFrame(self._scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING["xl"]))

        ctk.CTkLabel(
            header,
            text="⚙  Settings & Preferences",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Configure your AI assistant personality, API tokens, voice, and profile settings",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # 1. Profile Settings
        prof_card = GlassCard(self._scroll, title="👤 Profile")
        prof_card.pack(fill="x", pady=(0, SPACING["xl"]))

        prof_row = ctk.CTkFrame(prof_card.content, fg_color="transparent")
        prof_row.pack(fill="x", pady=(4, 0))

        ctk.CTkLabel(
            prof_row,
            text="User Display Name:",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        ).pack(side="left", padx=(0, 12))

        self.name_entry = ctk.CTkEntry(prof_row, width=220)
        self.name_entry.insert(0, DEFAULT_USER_NAME)
        self.name_entry.pack(side="left")

        # 2. AI Personality Mode
        pers_card = GlassCard(self._scroll, title="🤖 AI Personality Mode")
        pers_card.pack(fill="x", pady=(0, SPACING["xl"]))

        ctk.CTkLabel(
            pers_card.content,
            text="Select BUJJI AI's conversational tone & style:",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        self.pers_var = ctk.StringVar(value="friendly")
        personalities = ["friendly", "professional", "teacher", "motivator", "funny", "developer"]

        pers_frame = ctk.CTkFrame(pers_card.content, fg_color="transparent")
        pers_frame.pack(fill="x", pady=(8, 0))

        for p in personalities:
            rb = ctk.CTkRadioButton(
                pers_frame,
                text=p.capitalize(),
                variable=self.pers_var,
                value=p,
                fg_color=COLORS["accent_purple"],
            )
            rb.pack(side="left", padx=8)

        # 3. API Keys
        api_card = GlassCard(self._scroll, title="🔑 API Key Configuration")
        api_card.pack(fill="x", pady=(0, SPACING["xl"]))

        ctk.CTkLabel(
            api_card.content,
            text="Google Gemini API Key:",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        self.key_entry = ctk.CTkEntry(
            api_card.content,
            placeholder_text="Paste your GOOGLE_API_KEY here...",
            font=("Segoe UI", 12),
            show="•",
            height=36,
        )
        if GOOGLE_API_KEY:
            self.key_entry.insert(0, GOOGLE_API_KEY)
        self.key_entry.pack(fill="x", pady=(4, 0))

        # Save Button
        save_btn = ctk.CTkButton(
            self._scroll,
            text="💾 Save Settings",
            font=("Segoe UI", 14, "bold"),
            fg_color=COLORS["accent_purple"],
            hover_color=COLORS["accent_purple_hover"],
            height=44,
            command=self.save_settings,
        )
        save_btn.pack(anchor="w", pady=SPACING["md"])

        self.save_status = ctk.CTkLabel(
            self._scroll,
            text="",
            font=("Segoe UI", 12),
            text_color=COLORS["success"],
        )
        self.save_status.pack(anchor="w")

    def save_settings(self):
        new_name = self.name_entry.get().strip()
        new_pers = self.pers_var.get()
        new_key = self.key_entry.get().strip()

        if self.app:
            if new_key:
                self.app.ai_client.api_key = new_key
                self.app.ai_client.reset_chat(personality=new_pers)
            if new_name:
                self.app.user_name = new_name
                self.app.window.landing_page._greeting_label.configure(
                    text=f"{self.app.window.landing_page._get_greeting()}, {new_name}! 👋"
                )

        self.save_status.configure(text="✅ Settings saved successfully!")
