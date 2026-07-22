"""
Chat Page — ChatGPT-style conversation interface
===================================================
Full-featured chat UI with message bubbles, typing indicator,
input bar, and chat history sidebar.
"""

import threading
import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.chat_bubble import ChatBubble
from bujji.ui.components.typing_indicator import TypingIndicator


class ChatPage(ctk.CTkFrame):
    """
    ChatGPT-style conversation page with:
    - Scrollable message area
    - Chat bubbles (user + AI)
    - Typing indicator
    - Input bar with send + mic buttons
    - Chat history sidebar
    """

    def __init__(self, master, on_send=None, on_mic=None, on_new_chat=None, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)

        self._on_send = on_send
        self._on_mic = on_mic
        self._on_new_chat = on_new_chat

        # Main layout: history sidebar (left) + chat area (right)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ─── Chat History Sidebar ─────────────────────────────────────────
        self._history_panel = ctk.CTkFrame(
            self,
            width=220,
            fg_color=COLORS["bg_sidebar"],
            corner_radius=0,
            border_width=1,
            border_color=COLORS["border"],
        )
        self._history_panel.grid(row=0, column=0, sticky="ns")
        self._history_panel.pack_propagate(False)

        # New Chat button
        new_chat_btn = ctk.CTkButton(
            self._history_panel,
            text="＋  New Chat",
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent_purple"],
            hover_color=COLORS["accent_purple_hover"],
            text_color=COLORS["text_on_accent"],
            corner_radius=RADIUS["md"],
            height=38,
            command=self._handle_new_chat,
        )
        new_chat_btn.pack(fill="x", padx=SPACING["md"], pady=(SPACING["md"], SPACING["sm"]))

        # Search
        self._search_entry = ctk.CTkEntry(
            self._history_panel,
            placeholder_text="🔍 Search chats...",
            font=("Segoe UI", 12),
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_tertiary"],
            height=32,
            corner_radius=RADIUS["md"],
        )
        self._search_entry.pack(fill="x", padx=SPACING["md"], pady=(0, SPACING["sm"]))

        # Chat list
        self._chat_list = ctk.CTkScrollableFrame(
            self._history_panel,
            fg_color="transparent",
            scrollbar_button_color=COLORS["scrollbar_thumb"],
        )
        self._chat_list.pack(fill="both", expand=True, padx=4, pady=4)

        # Placeholder
        self._history_placeholder = ctk.CTkLabel(
            self._chat_list,
            text="No chat history yet",
            font=("Segoe UI", 11),
            text_color=COLORS["text_tertiary"],
        )
        self._history_placeholder.pack(pady=SPACING["xl"])

        # ─── Chat Area ────────────────────────────────────────────────────
        chat_area = ctk.CTkFrame(self, fg_color="transparent")
        chat_area.grid(row=0, column=1, sticky="nsew")
        chat_area.rowconfigure(0, weight=1)
        chat_area.columnconfigure(0, weight=1)

        # Chat header
        header = ctk.CTkFrame(chat_area, height=50, fg_color=COLORS["bg_secondary"],
                              corner_radius=0, border_width=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        self._chat_title = ctk.CTkLabel(
            header,
            text="💬  New Conversation",
            font=("Segoe UI", 15, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        self._chat_title.pack(side="left", padx=SPACING["lg"], pady=SPACING["md"])

        # Personality badge
        self._personality_badge = ctk.CTkLabel(
            header,
            text="🤝 Friendly",
            font=("Segoe UI", 11),
            text_color=COLORS["accent_cyan"],
            fg_color=COLORS["bg_card"],
            corner_radius=RADIUS["sm"],
            padx=8,
            pady=2,
        )
        self._personality_badge.pack(side="right", padx=SPACING["lg"])

        # Message area (scrollable)
        self._messages_frame = ctk.CTkScrollableFrame(
            chat_area,
            fg_color="transparent",
            scrollbar_button_color=COLORS["scrollbar_thumb"],
            scrollbar_button_hover_color=COLORS["border_light"],
        )
        self._messages_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        chat_area.rowconfigure(1, weight=1)

        # Welcome message
        self._show_welcome()

        # Typing indicator (hidden initially)
        self._typing_indicator = TypingIndicator(self._messages_frame)

        # ─── Input Bar ────────────────────────────────────────────────────
        input_bar = ctk.CTkFrame(
            chat_area,
            height=70,
            fg_color=COLORS["bg_secondary"],
            corner_radius=0,
        )
        input_bar.grid(row=2, column=0, sticky="ew")
        input_bar.grid_propagate(False)

        input_inner = ctk.CTkFrame(input_bar, fg_color="transparent")
        input_inner.pack(fill="x", padx=SPACING["lg"], pady=SPACING["md"])
        input_inner.columnconfigure(0, weight=1)

        # Text input
        self._input_field = ctk.CTkEntry(
            input_inner,
            placeholder_text="Type a message to BUJJI...",
            font=("Segoe UI", 13),
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_tertiary"],
            height=40,
            corner_radius=RADIUS["lg"],
        )
        self._input_field.grid(row=0, column=0, sticky="ew", padx=(0, SPACING["sm"]))
        self._input_field.bind("<Return>", self._handle_send)

        # Mic button
        mic_btn = ctk.CTkButton(
            input_inner,
            text="🎤",
            width=40,
            height=40,
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["bg_card_hover"],
            corner_radius=RADIUS["full"],
            font=("Segoe UI", 18),
            command=self._handle_mic,
        )
        mic_btn.grid(row=0, column=1, padx=(0, SPACING["sm"]))

        # Send button
        send_btn = ctk.CTkButton(
            input_inner,
            text="➤",
            width=40,
            height=40,
            fg_color=COLORS["accent_purple"],
            hover_color=COLORS["accent_purple_hover"],
            corner_radius=RADIUS["full"],
            font=("Segoe UI", 18),
            command=lambda: self._handle_send(None),
        )
        send_btn.grid(row=0, column=2)

    def _show_welcome(self):
        """Show welcome message in empty chat."""
        welcome = ctk.CTkFrame(self._messages_frame, fg_color="transparent")
        welcome.pack(fill="x", pady=SPACING["3xl"])

        ctk.CTkLabel(
            welcome,
            text="🤖",
            font=("Segoe UI", 48),
        ).pack()

        ctk.CTkLabel(
            welcome,
            text="Hello! I'm BUJJI AI",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORS["text_primary"],
        ).pack(pady=(SPACING["md"], SPACING["xs"]))

        ctk.CTkLabel(
            welcome,
            text="Your intelligent desktop companion.\nAsk me anything, give me a task, or just chat!",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            justify="center",
        ).pack()

        # Suggestion chips
        suggestions = [
            "What can you do?",
            "Tell me a joke",
            "Explain Python decorators",
            "What's the weather?",
        ]

        chips_frame = ctk.CTkFrame(welcome, fg_color="transparent")
        chips_frame.pack(pady=SPACING["xl"])

        for suggestion in suggestions:
            chip = ctk.CTkButton(
                chips_frame,
                text=suggestion,
                font=("Segoe UI", 11),
                fg_color=COLORS["bg_card"],
                hover_color=COLORS["bg_card_hover"],
                text_color=COLORS["text_secondary"],
                corner_radius=RADIUS["xl"],
                height=32,
                border_width=1,
                border_color=COLORS["border"],
                command=lambda s=suggestion: self._send_suggestion(s),
            )
            chip.pack(side="left", padx=4)

    def _send_suggestion(self, text):
        """Send a suggestion chip as a message."""
        self._input_field.delete(0, "end")
        self._input_field.insert(0, text)
        self._handle_send(None)

    def _handle_send(self, event):
        """Handle sending a message."""
        text = self._input_field.get().strip()
        if not text:
            return

        self._input_field.delete(0, "end")

        # Clear welcome message on first send
        if hasattr(self, "_welcome_cleared") and not self._welcome_cleared:
            pass
        self._welcome_cleared = True

        # Add user bubble
        self.add_message(text, is_user=True)

        # Notify handler
        if self._on_send:
            self._on_send(text)

    def _handle_mic(self):
        """Handle mic button click."""
        if self._on_mic:
            self._on_mic()

    def _handle_new_chat(self):
        """Handle new chat button click."""
        self.clear_messages()
        if self._on_new_chat:
            self._on_new_chat()

    def add_message(self, text, is_user=True, timestamp=None):
        """Add a message bubble to the chat."""
        bubble = ChatBubble(
            self._messages_frame,
            message=text,
            is_user=is_user,
            timestamp=timestamp,
            on_regenerate=None if is_user else (lambda: self._on_send("regenerate") if self._on_send else None),
        )
        bubble.pack(fill="x")
        # Auto-scroll to bottom
        self._messages_frame._parent_canvas.yview_moveto(1.0)

    def show_typing(self):
        """Show the typing indicator."""
        self._typing_indicator.start()
        self._messages_frame._parent_canvas.yview_moveto(1.0)

    def hide_typing(self):
        """Hide the typing indicator."""
        self._typing_indicator.stop()

    def clear_messages(self):
        """Clear all messages and show welcome again."""
        for widget in self._messages_frame.winfo_children():
            widget.destroy()
        self._typing_indicator = TypingIndicator(self._messages_frame)
        self._show_welcome()
        self._chat_title.configure(text="💬  New Conversation")

    def set_chat_title(self, title):
        """Update the chat header title."""
        self._chat_title.configure(text=f"💬  {title}")

    def set_personality_badge(self, personality):
        """Update the personality badge."""
        icons = {
            "professional": "💼",
            "friendly": "🤝",
            "teacher": "📚",
            "motivator": "💪",
            "funny": "😄",
            "developer": "💻",
        }
        icon = icons.get(personality, "🤝")
        self._personality_badge.configure(text=f"{icon} {personality.capitalize()}")

    def update_history(self, conversations):
        """Update the chat history sidebar."""
        for widget in self._chat_list.winfo_children():
            widget.destroy()

        if not conversations:
            ctk.CTkLabel(
                self._chat_list,
                text="No chat history yet",
                font=("Segoe UI", 11),
                text_color=COLORS["text_tertiary"],
            ).pack(pady=SPACING["xl"])
            return

        for conv in conversations:
            btn = ctk.CTkButton(
                self._chat_list,
                text=f"💬 {conv.get('title', 'Untitled')}",
                font=("Segoe UI", 11),
                fg_color="transparent",
                hover_color=COLORS["bg_sidebar_hover"],
                text_color=COLORS["text_secondary"],
                anchor="w",
                height=32,
                corner_radius=RADIUS["sm"],
            )
            btn.pack(fill="x", pady=1)
