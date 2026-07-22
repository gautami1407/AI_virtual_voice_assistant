"""
Typing Indicator — Three-dot "BUJJI is thinking" animation
============================================================
Animated dots that pulse to indicate the AI is processing.
"""

import customtkinter as ctk
from bujji.ui.theme import COLORS, ANIMATION


class TypingIndicator(ctk.CTkFrame):
    """
    Three-dot typing animation similar to messaging apps.
    Shows "BUJJI is thinking..." with pulsing dots.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._animating = False
        self._dot_index = 0

        # Container row
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=4)

        # Avatar
        ctk.CTkLabel(
            row,
            text="🤖",
            font=("Segoe UI", 20),
            width=36,
            height=36,
            fg_color=COLORS["bg_secondary"],
            corner_radius=9999,
        ).pack(side="left", padx=(0, 8))

        # Bubble
        bubble = ctk.CTkFrame(
            row,
            fg_color=COLORS["chat_ai_bg"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        bubble.pack(side="left", padx=(4, 0))

        # Inner content
        inner = ctk.CTkFrame(bubble, fg_color="transparent")
        inner.pack(padx=16, pady=10)

        # Label text
        self._label = ctk.CTkLabel(
            inner,
            text="BUJJI is thinking",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self._label.pack(side="left")

        # Dot labels
        self._dots = []
        for i in range(3):
            dot = ctk.CTkLabel(
                inner,
                text="●",
                font=("Segoe UI", 14),
                text_color=COLORS["text_tertiary"],
                width=12,
            )
            dot.pack(side="left", padx=1)
            self._dots.append(dot)

    def start(self):
        """Start the typing animation."""
        self._animating = True
        self._dot_index = 0
        self.pack(fill="x")  # Show the widget
        self._animate()

    def stop(self):
        """Stop and hide the typing indicator."""
        self._animating = False
        self.pack_forget()  # Hide the widget

    def _animate(self):
        if not self._animating:
            return

        # Reset all dots
        for dot in self._dots:
            dot.configure(text_color=COLORS["text_tertiary"])

        # Highlight current dot
        active = self._dot_index % 3
        self._dots[active].configure(text_color=COLORS["accent_purple"])

        self._dot_index += 1
        self.after(400, self._animate)
