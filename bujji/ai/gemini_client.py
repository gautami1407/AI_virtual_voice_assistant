"""
Gemini Client — Gemini API Wrapper with Conversation Memory
============================================================
Handles interaction with Google Gemini API, keeping context history,
retry logic, automatic model fallback (1.5-flash, 1.5-pro, 2.0-flash),
and personality prompt injection.
"""

import os
import time
from bujji.config import GOOGLE_API_KEY, DEFAULT_GEMINI_MODEL
from bujji.ai.personality import get_system_prompt

GENAI_AVAILABLE = False
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


FALLBACK_MODELS = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]


class GeminiClient:
    """
    Wrapper for Google Gemini API with conversational context memory and
    automatic model fallback.
    """

    def __init__(self, api_key=None, model_name=DEFAULT_GEMINI_MODEL, personality="friendly"):
        self.api_key = api_key or GOOGLE_API_KEY
        self.model_name = model_name
        self.personality = personality
        self.model = None
        self.chat_session = None

        self._configure()

    def _configure(self, model_override=None):
        """Initialize Google Generative AI SDK."""
        if not self.api_key:
            print("[WARNING] GOOGLE_API_KEY is not set in environment or config.")
            return

        if not GENAI_AVAILABLE:
            print("[WARNING] google-generativeai package is not installed.")
            return

        target_model = model_override or self.model_name
        try:
            genai.configure(api_key=self.api_key)
            system_instruction = get_system_prompt(self.personality)

            self.model = genai.GenerativeModel(
                model_name=target_model,
                system_instruction=system_instruction,
            )
            self.chat_session = self.model.start_chat(history=[])
            self.model_name = target_model
        except Exception as e:
            print(f"[ERROR] Failed to initialize Gemini model '{target_model}': {e}")

    def generate_response(self, prompt, history=None):
        """
        Generate response for user prompt with conversation history and fallback models.
        """
        if not self.api_key:
            return (
                "⚠️ **Google Gemini API Key is missing.**\n\n"
                "Please add your `GOOGLE_API_KEY` to the `.env` file or Settings to enable AI responses."
            )

        if not self.model or not self.chat_session:
            self._configure()

        # Attempt sending with current model and fallback models
        models_to_try = [self.model_name] + [m for m in FALLBACK_MODELS if m != self.model_name]

        for m_name in models_to_try:
            try:
                if self.model_name != m_name:
                    self._configure(model_override=m_name)

                if self.chat_session:
                    response = self.chat_session.send_message(prompt)
                    if response and hasattr(response, 'text') and response.text:
                        return response.text
            except Exception as e:
                error_msg = str(e)

                # Check if it's invalid key
                if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
                    return "❌ **Invalid API Key**: Please check your `GOOGLE_API_KEY` in `.env` or Settings."

                # If quota/rate-limit hit on this model, continue to try next fallback model
                if "429" in error_msg or "quota" in error_msg.lower() or "limit: 0" in error_msg.lower():
                    print(f"[Gemini Quota Warning] Model {m_name} hit rate limit. Trying fallback model...")
                    continue
                else:
                    print(f"[Gemini Error] Model {m_name} failed: {error_msg}")

        # If all models failed due to 429 rate limits
        return (
            "⏱️ **API Rate Limit Exceeded (429)**\n\n"
            "The Google Gemini free tier rate limit was reached.\n"
            "Please wait **~20 seconds** before your next request, or update your API key in **Settings**."
        )

    def reset_chat(self, personality=None):
        """Reset conversation session (start clean chat memory)."""
        if personality:
            self.personality = personality
        self._configure()
