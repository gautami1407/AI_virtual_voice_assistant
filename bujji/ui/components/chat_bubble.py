"""
Chat Bubble — Message bubble component for the chat interface
==============================================================
Renders user and AI messages with avatar, timestamp, and action buttons.
"""

import customtkinter as ctk
from datetime import datetime
from bujji.ui.theme import COLORS, FONTS, RADIUS, SPACING


class ChatBubble(ctk.CTkFrame):
    """
    A chat message bubble with:
    - Avatar icon (emoji)
    - Message text with wrapping
    - Timestamp
    - Copy button on hover
    - Different styling for user vs AI messages
    """

    def __init__(
        self,
        master,
        message,
        is_user=True,
        timestamp=None,
        on_copy=None,
        on_regenerate=None,
        max_width=600,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_copy = on_copy
        self._on_regenerate = on_regenerate
        self._message = message
        self._is_user = is_user

        timestamp = timestamp or datetime.now().strftime("%I:%M %p")

        # Configure alignment
        anchor_side = "e" if is_user else "w"
        bubble_color = COLORS["chat_user_bg"] if is_user else COLORS["chat_ai_bg"]
        text_color = COLORS["chat_user_text"] if is_user else COLORS["chat_ai_text"]
        avatar = "👤" if is_user else "🤖"
        name = "You" if is_user else "BUJJI"

        # Outer row (avatar + bubble)
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=(4, 4), padx=SPACING["md"])

        if is_user:
            # Push content to the right
            row.columnconfigure(0, weight=1)
            col_bubble = 1
            col_avatar = 2
        else:
            # Push content to the left
            row.columnconfigure(2, weight=1)
            col_avatar = 0
            col_bubble = 1

        # Avatar
        avatar_label = ctk.CTkLabel(
            row,
            text=avatar,
            font=("Segoe UI", 20),
            width=36,
            height=36,
            fg_color=COLORS["bg_secondary"],
            corner_radius=RADIUS["full"],
            text_color=COLORS["text_primary"],
        )
        avatar_label.grid(row=0, column=col_avatar, padx=(4, 4), sticky="n")

        # Bubble container
        bubble = ctk.CTkFrame(
            row,
            fg_color=bubble_color,
            corner_radius=RADIUS["lg"],
            border_width=1,
            border_color=COLORS["border"],
        )
        bubble.grid(row=0, column=col_bubble, sticky="w" if not is_user else "e", padx=(4, 4))

        # Name + timestamp header
        header = ctk.CTkFrame(bubble, fg_color="transparent")
        header.pack(fill="x", padx=SPACING["md"], pady=(SPACING["sm"], 0))

        ctk.CTkLabel(
            header,
            text=name,
            font=("Segoe UI", 12, "bold"),
            text_color=COLORS["text_accent"] if not is_user else COLORS["text_primary"],
            anchor="w",
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=timestamp,
            font=("Segoe UI", 10),
            text_color=COLORS["text_tertiary"],
            anchor="e",
        ).pack(side="right", padx=(SPACING["md"], 0))

        # Message text
        msg_label = ctk.CTkLabel(
            bubble,
            text=message,
            font=("Segoe UI", 13),
            text_color=text_color,
            wraplength=max_width,
            justify="left",
            anchor="w",
        )
        msg_label.pack(fill="x", padx=SPACING["md"], pady=(SPACING["xs"], SPACING["sm"]))

        # Action buttons (shown on hover for AI messages)
        if not is_user:
            self._actions_frame = ctk.CTkFrame(bubble, fg_color="transparent", height=24)
            self._actions_frame.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["sm"]))

            copy_btn = ctk.CTkButton(
                self._actions_frame,
                text="📋 Copy",
                font=("Segoe UI", 10),
                width=60,
                height=22,
                fg_color="transparent",
                hover_color=COLORS["bg_sidebar_hover"],
                text_color=COLORS["text_secondary"],
                corner_radius=RADIUS["sm"],
                command=self._copy_message,
            )
            copy_btn.pack(side="left", padx=(0, 4))

            if on_regenerate:
                regen_btn = ctk.CTkButton(
                    self._actions_frame,
                    text="🔄 Regenerate",
                    font=("Segoe UI", 10),
                    width=90,
                    height=22,
                    fg_color="transparent",
                    hover_color=COLORS["bg_sidebar_hover"],
                    text_color=COLORS["text_secondary"],
                    corner_radius=RADIUS["sm"],
                    command=on_regenerate,
                )
                regen_btn.pack(side="left", padx=(0, 4))

    def _copy_message(self):
        """Copy message to clipboard."""
        try:
            self.clipboard_clear()
            self.clipboard_append(self._message)
            if self._on_copy:
                self._on_copy(self._message)
        except Exception:
            pass
