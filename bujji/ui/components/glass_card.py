"""
Glass Card — Glassmorphism-inspired card component
===================================================
A reusable card widget with semi-transparent background,
subtle border, and rounded corners for the dark theme.
"""

import customtkinter as ctk
from bujji.ui.theme import COLORS, RADIUS, SPACING, FONT_BODY


class GlassCard(ctk.CTkFrame):
    """
    A glassmorphism-style card with rounded corners, subtle border,
    and semi-transparent feel against the dark background.
    """

    def __init__(
        self,
        master,
        title=None,
        subtitle=None,
        corner_radius=None,
        padding=None,
        hover_effect=True,
        **kwargs
    ):
        # Defaults
        corner_radius = corner_radius or RADIUS["lg"]
        self._padding = padding or SPACING["lg"]
        self._hover_effect = hover_effect
        self._base_color = COLORS["bg_card"]
        self._hover_color = COLORS["bg_card_hover"]

        super().__init__(
            master,
            corner_radius=corner_radius,
            fg_color=self._base_color,
            border_width=1,
            border_color=COLORS["border"],
            **kwargs,
        )

        # Internal content frame with padding
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=self._padding, pady=self._padding)

        # Optional title
        if title:
            self._title_label = ctk.CTkLabel(
                self.content,
                text=title,
                font=("Segoe UI", 16, "bold"),
                text_color=COLORS["text_primary"],
                anchor="w",
            )
            self._title_label.pack(fill="x", pady=(0, 4))

        # Optional subtitle
        if subtitle:
            self._subtitle_label = ctk.CTkLabel(
                self.content,
                text=subtitle,
                font=("Segoe UI", 12),
                text_color=COLORS["text_secondary"],
                anchor="w",
            )
            self._subtitle_label.pack(fill="x", pady=(0, 8))

        # Hover effects
        if self._hover_effect:
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        self.configure(
            fg_color=self._hover_color,
            border_color=COLORS["border_light"],
        )

    def _on_leave(self, event=None):
        self.configure(
            fg_color=self._base_color,
            border_color=COLORS["border"],
        )
