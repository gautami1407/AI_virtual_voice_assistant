"""
Quick Actions — Grid of action buttons for the landing page
=============================================================
Renders a responsive grid of styled action buttons with emoji icons.
"""

import customtkinter as ctk
from bujji.ui.theme import COLORS, RADIUS, SPACING


class QuickActionButton(ctk.CTkFrame):
    """A single quick action button with icon and label."""

    def __init__(self, master, icon, label, on_click=None, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["bg_card"],
            corner_radius=RADIUS["lg"],
            border_width=1,
            border_color=COLORS["border"],
            cursor="hand2",
            **kwargs,
        )

        self._on_click = on_click
        self._base_color = COLORS["bg_card"]
        self._hover_color = COLORS["bg_card_hover"]

        # Internal padding
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(padx=SPACING["md"], pady=SPACING["md"])

        # Icon
        self._icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=("Segoe UI", 28),
        )
        self._icon_label.pack()

        # Label
        self._text_label = ctk.CTkLabel(
            inner,
            text=label,
            font=("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
        )
        self._text_label.pack(pady=(4, 0))

        # Bind click to all children
        for widget in [self, inner, self._icon_label, self._text_label]:
            widget.bind("<Button-1>", self._handle_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _handle_click(self, event=None):
        if self._on_click:
            self._on_click()

    def _on_enter(self, event=None):
        self.configure(fg_color=self._hover_color, border_color=COLORS["accent_purple"])
        self._text_label.configure(text_color=COLORS["text_primary"])

    def _on_leave(self, event=None):
        self.configure(fg_color=self._base_color, border_color=COLORS["border"])
        self._text_label.configure(text_color=COLORS["text_secondary"])


class QuickActionsGrid(ctk.CTkFrame):
    """A grid of QuickActionButton widgets."""

    def __init__(self, master, actions, columns=4, on_action=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_action = on_action

        for i, action in enumerate(actions):
            row = i // columns
            col = i % columns

            self.columnconfigure(col, weight=1)

            btn = QuickActionButton(
                self,
                icon=action["icon"],
                label=action["label"],
                on_click=lambda a=action["action"]: self._dispatch(a),
            )
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

    def _dispatch(self, action_key):
        if self._on_action:
            self._on_action(action_key)
