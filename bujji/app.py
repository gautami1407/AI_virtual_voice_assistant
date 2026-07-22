"""
Application Controller — BUJJI AI Core Controller
===================================================
Central orchestrator connecting UI, Gemini AI, Speech engine, Listener,
and Data Persistence layer.
"""

import sys
import os
import threading

# Add parent directory to sys.path if missing so running inside bujji folder works
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from bujji.config import DEFAULT_USER_NAME
from bujji.data.database import DatabaseManager
from bujji.ai.gemini_client import GeminiClient
from bujji.ai.conversation import ConversationManager
from bujji.voice.speech_engine import SpeechEngine
from bujji.voice.listener import VoiceListener
from bujji.ui.app_window import AppWindow


class BujjiApp:
    """
    Central Controller for BUJJI AI application.
    """

    def __init__(self):
        # 1. Database
        self.db = DatabaseManager()

        # 2. AI & Conversation Manager
        self.ai_client = GeminiClient()
        self.conv_manager = ConversationManager(self.db)

        # 3. Voice Subsystems
        self.speech_engine = SpeechEngine()
        self.listener = VoiceListener(
            on_command_callback=self._handle_voice_command,
            on_status_callback=self._handle_voice_status,
        )

        # 4. User Interface Window
        self.user_name = DEFAULT_USER_NAME
        self.window = AppWindow(
            user_name=self.user_name,
            on_navigate_callback=self._on_navigate,
            app_controller=self,
        )

        # Connect UI callbacks
        self.window.chat_page._on_send = self.process_chat_message
        self.window.chat_page._on_mic = self.trigger_voice_input
        self.window.chat_page._on_new_chat = self.new_chat_session
        self.window.voice_page._on_mic_toggle = self.toggle_voice_listening

        # Sync initial UI state
        self._refresh_chat_history_ui()

    def process_chat_message(self, text):
        """Process a text chat message from the user."""
        if not text or not text.strip():
            return

        # Record in conversation DB
        self.conv_manager.add_message("user", text)

        # Show typing in UI
        self.window.chat_page.show_typing()

        def _ai_thread():
            # Get Gemini response
            response = self.ai_client.generate_response(text)

            # Record AI response in DB
            self.conv_manager.add_message("model", response)

            # Update UI on main thread
            self.window.after(0, lambda: self._on_ai_response(response))

        threading.Thread(target=_ai_thread, daemon=True).start()

    def _on_ai_response(self, response_text):
        """Callback when AI response is ready."""
        self.window.chat_page.hide_typing()
        self.window.chat_page.add_message(response_text, is_user=False)
        self.window.voice_page.add_transcript_entry("BUJJI", response_text)
        self._refresh_chat_history_ui()

        # Speak AI response if on voice page or voice mode is enabled
        if self.window.current_page_key == "voice":
            self.speech_engine.speak(response_text)

    def trigger_voice_input(self):
        """Trigger one-shot voice listening from mic button."""
        self.window.show_page("voice")

        def _voice_thread():
            cmd = self.listener.listen_once()
            if cmd:
                self.window.after(0, lambda: self._on_voice_captured(cmd))

        threading.Thread(target=_voice_thread, daemon=True).start()

    def _on_voice_captured(self, text):
        """Handle captured speech text."""
        self.window.voice_page.add_transcript_entry("You", text)
        self.window.chat_page.add_message(text, is_user=True)
        self.process_chat_message(text)

    def toggle_voice_listening(self, active):
        """Toggle background wake-word listening loop."""
        if active:
            self.listener.start_wake_word_loop()
        else:
            self.listener.stop()

    def _handle_voice_command(self, cmd_text):
        """Callback from voice listener when command is recognized."""
        self.window.after(0, lambda: self._on_voice_captured(cmd_text))

    def _handle_voice_status(self, status):
        """Callback for voice listener status updates."""
        self.window.after(0, lambda: self.window.voice_page.set_status(status))

    def new_chat_session(self):
        """Start a brand new conversation."""
        self.conv_manager.start_new_conversation()
        self.ai_client.reset_chat()
        self.window.chat_page.clear_messages()
        self._refresh_chat_history_ui()

    def _refresh_chat_history_ui(self):
        """Update chat history list on sidebar and landing page."""
        history = self.conv_manager.list_conversations()
        self.window.chat_page.update_history(history)
        self.window.landing_page.update_recent_conversations(history)

    def _on_navigate(self, page_key):
        """Page navigation event handler."""
        pass

    def run(self):
        """Start main loop."""
        self.window.mainloop()


if __name__ == "__main__":
    app = BujjiApp()
    app.run()
