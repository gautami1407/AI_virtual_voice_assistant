"""
Conversation Manager — Manages active chat sessions and database syncing
========================================================================
Handles chat creation, history management, persistence, title generation, and export.
"""

import uuid
from datetime import datetime


class ConversationManager:
    """
    Manages active conversations, loads past sessions from SQLite,
    and updates chat history.
    """

    def __init__(self, db_manager):
        self.db = db_manager
        self.current_conv_id = None
        self.start_new_conversation()

    def start_new_conversation(self, personality="friendly"):
        """Create a new conversation session."""
        self.current_conv_id = str(uuid.uuid4())
        title = "New Conversation"
        self.db.save_conversation(self.current_conv_id, title, personality)
        return self.current_conv_id

    def add_message(self, role, content):
        """Add user or assistant message to current conversation."""
        if not self.current_conv_id:
            self.start_new_conversation()

        self.db.add_message(self.current_conv_id, role, content)

        # Auto-update title if it's the first user message
        messages = self.db.get_messages(self.current_conv_id)
        if len(messages) == 1 and role == "user":
            # Generate short title from first prompt
            short_title = content[:30] + ("..." if len(content) > 30 else "")
            self.db.save_conversation(self.current_conv_id, short_title)

    def get_current_messages(self):
        """Get message list for current conversation."""
        if not self.current_conv_id:
            return []
        return self.db.get_messages(self.current_conv_id)

    def load_conversation(self, conv_id):
        """Switch active conversation session."""
        self.current_conv_id = conv_id
        return self.get_current_messages()

    def list_conversations(self):
        """List all past conversation summaries for UI list."""
        convs = self.db.get_conversations()
        result = []
        for c in convs:
            msgs = self.db.get_messages(c["id"])
            preview = msgs[-1]["content"][:50] if msgs else "No messages"
            result.append({
                "id": c["id"],
                "title": c["title"],
                "personality": c.get("personality", "friendly"),
                "updated_at": c.get("updated_at", ""),
                "preview": preview,
            })
        return result

    def delete_conversation(self, conv_id):
        """Delete conversation and its messages."""
        self.db.delete_conversation(conv_id)
        if self.current_conv_id == conv_id:
            self.start_new_conversation()
