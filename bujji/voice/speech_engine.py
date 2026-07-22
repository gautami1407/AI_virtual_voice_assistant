"""
Speech Engine — Text-To-Speech (TTS) Wrapper
=============================================
Non-blocking TTS engine using pyttsx3, supporting voice selection,
rate adjustment, and queue management.
"""

import threading
import queue
import pyttsx3
from bujji.config import DEFAULT_VOICE_INDEX, DEFAULT_VOICE_RATE, DEFAULT_VOICE_VOLUME


class SpeechEngine:
    """
    Thread-safe TTS engine using pyttsx3.
    """

    def __init__(self, voice_index=DEFAULT_VOICE_INDEX, rate=DEFAULT_VOICE_RATE, volume=DEFAULT_VOICE_VOLUME):
        self.voice_index = voice_index
        self.rate = rate
        self.volume = volume
        self.speech_queue = queue.Queue()
        self._is_speaking = False
        self._thread = None
        self.on_speech_start = None
        self.on_speech_end = None

    def speak(self, text, callback=None):
        """Queue text to speak in a background thread."""
        if not text or not text.strip():
            return

        def _run():
            self._is_speaking = True
            if self.on_speech_start:
                self.on_speech_start()
            try:
                engine = pyttsx3.init()
                voices = engine.getProperty("voices")
                if voices and self.voice_index < len(voices):
                    engine.setProperty("voice", voices[self.voice_index].id)
                engine.setProperty("rate", self.rate)
                engine.setProperty("volume", self.volume)

                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"[TTS Error] {e}")
            finally:
                self._is_speaking = False
                if self.on_speech_end:
                    self.on_speech_end()
                if callback:
                    callback()

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def is_speaking(self):
        return self._is_speaking
