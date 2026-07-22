"""
Voice Listener — Speech Recognition Wrapper
=============================================
Manages microphone input, Google Speech Recognition API, wake word detection,
and ambient noise cancellation.
"""

import threading
import speech_recognition as sr
from bujji.config import WAKE_WORDS


class VoiceListener:
    """
    Speech recognition listener supporting wake word detection
    and one-shot voice command capture.
    """

    def __init__(self, on_command_callback=None, on_status_callback=None):
        self.recognizer = sr.Recognizer()
        self.on_command_callback = on_command_callback
        self.on_status_callback = on_status_callback
        self.is_listening = False
        self._listen_thread = None
        self._stop_event = threading.Event()

    def listen_once(self, timeout=5, phrase_time_limit=8):
        """Capture a single audio command from the microphone."""
        try:
            if self.on_status_callback:
                self.on_status_callback("listening")

            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )

            if self.on_status_callback:
                self.on_status_callback("processing")

            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            if self.on_status_callback:
                self.on_status_callback("idle")
            return None
        except sr.UnknownValueError:
            if self.on_status_callback:
                self.on_status_callback("idle")
            return None
        except Exception as e:
            print(f"[Listener Error] {e}")
            if self.on_status_callback:
                self.on_status_callback("error")
            return None

    def start_wake_word_loop(self):
        """Start background wake word detection loop."""
        if self.is_listening:
            return

        self.is_listening = True
        self._stop_event.clear()

        def _loop():
            while not self._stop_event.is_set():
                text = self.listen_once(timeout=3, phrase_time_limit=5)
                if text:
                    # Check if wake word detected
                    if any(w in text for w in WAKE_WORDS):
                        if self.on_status_callback:
                            self.on_status_callback("listening")
                        # Capture actual command after wake word
                        cmd = self.listen_once(timeout=5, phrase_time_limit=10)
                        if cmd and self.on_command_callback:
                            self.on_command_callback(cmd)
                    elif self.on_command_callback:
                        # Direct speech without explicit wake word prefix
                        self.on_command_callback(text)

        self._listen_thread = threading.Thread(target=_loop, daemon=True)
        self._listen_thread.start()

    def stop(self):
        """Stop background listening loop."""
        self.is_listening = False
        self._stop_event.set()
        if self.on_status_callback:
            self.on_status_callback("idle")
