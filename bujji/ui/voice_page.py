"""
Voice Page — Voice interaction screen with waveform visualization
===================================================================
Full-screen voice interaction UI with animated waveform,
mic orb, status text, and conversation transcript.
"""

import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.waveform import WaveformVisualizer
from bujji.ui.components.floating_orb import FloatingOrb


class VoicePage(ctk.CTkFrame):
    """
    Voice interaction page with:
    - Large animated waveform
    - Central microphone orb
    - Status indicator (Idle / Listening / Processing / Speaking)
    - Wake word hint
    - Conversation transcript
    """

    def __init__(self, master, on_mic_toggle=None, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)

        self._on_mic_toggle = on_mic_toggle
        self._is_listening = False

        # ─── Top: Voice Visualization Area ────────────────────────────────
        viz_area = ctk.CTkFrame(self, fg_color="transparent")
        viz_area.pack(fill="x", pady=(SPACING["3xl"], SPACING["xl"]))

        # Title
        ctk.CTkLabel(
            viz_area,
            text="Voice Chat",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
        ).pack()

        ctk.CTkLabel(
            viz_area,
            text='Say "Hey Bujji" or click the microphone to start',
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
        ).pack(pady=(4, SPACING["xl"]))

        # Waveform
        self._waveform = WaveformVisualizer(
            viz_area,
            width=500,
            height=100,
            bar_count=50,
        )
        self._waveform.pack(pady=SPACING["md"])
        self._waveform.start()

        # Mic Orb
        self._orb = FloatingOrb(
            viz_area,
            size=72,
            on_click=self._toggle_mic,
        )
        self._orb.pack(pady=SPACING["lg"])

        # Status
        self._status_label = ctk.CTkLabel(
            viz_area,
            text="● Idle — Waiting for wake word",
            font=("Segoe UI", 14, "bold"),
            text_color=COLORS["text_tertiary"],
        )
        self._status_label.pack()

        # ─── Bottom: Transcript ───────────────────────────────────────────
        transcript_section = ctk.CTkFrame(self, fg_color="transparent")
        transcript_section.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["lg"])

        ctk.CTkLabel(
            transcript_section,
            text="Conversation Transcript",
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(0, SPACING["sm"]))

        # Transcript scroll area
        self._transcript = ctk.CTkScrollableFrame(
            transcript_section,
            fg_color=COLORS["bg_secondary"],
            corner_radius=RADIUS["lg"],
            border_width=1,
            border_color=COLORS["border"],
            scrollbar_button_color=COLORS["scrollbar_thumb"],
        )
        self._transcript.pack(fill="both", expand=True)

        # Empty state
        self._empty_transcript = ctk.CTkLabel(
            self._transcript,
            text="Voice transcript will appear here...",
            font=("Segoe UI", 12),
            text_color=COLORS["text_tertiary"],
        )
        self._empty_transcript.pack(pady=SPACING["xl"])

    def _toggle_mic(self):
        """Toggle microphone listening state."""
        self._is_listening = not self._is_listening

        if self._is_listening:
            self.set_status("listening")
            self._waveform.set_active(True)
            self._orb.set_active(True)
        else:
            self.set_status("idle")
            self._waveform.set_active(False)
            self._orb.set_active(False)

        if self._on_mic_toggle:
            self._on_mic_toggle(self._is_listening)

    def set_status(self, status):
        """Update the voice status indicator."""
        statuses = {
            "idle": ("● Idle — Waiting for wake word", COLORS["text_tertiary"]),
            "listening": ("● Listening...", COLORS["accent_neon"]),
            "processing": ("● Processing your request...", COLORS["accent_cyan"]),
            "speaking": ("● BUJJI is speaking...", COLORS["accent_purple"]),
            "error": ("● Error — Please try again", COLORS["error"]),
        }
        text, color = statuses.get(status, statuses["idle"])
        self._status_label.configure(text=text, text_color=color)

    def add_transcript_entry(self, speaker, text):
        """Add an entry to the transcript."""
        # Remove empty state on first entry
        if hasattr(self, "_empty_transcript") and self._empty_transcript.winfo_exists():
            self._empty_transcript.destroy()

        entry = ctk.CTkFrame(self._transcript, fg_color="transparent")
        entry.pack(fill="x", padx=SPACING["md"], pady=4)

        is_user = speaker.lower() in ("you", "user")
        color = COLORS["accent_cyan"] if is_user else COLORS["accent_purple"]
        icon = "👤" if is_user else "🤖"

        ctk.CTkLabel(
            entry,
            text=f"{icon} {speaker}",
            font=("Segoe UI", 12, "bold"),
            text_color=color,
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            entry,
            text=text,
            font=("Segoe UI", 12),
            text_color=COLORS["text_primary"],
            anchor="w",
            wraplength=500,
            justify="left",
        ).pack(fill="x", padx=(24, 0))

        # Separator
        ctk.CTkFrame(
            self._transcript,
            height=1,
            fg_color=COLORS["border"],
        ).pack(fill="x", padx=SPACING["md"], pady=4)

        # Auto scroll
        self._transcript._parent_canvas.yview_moveto(1.0)

    def set_waveform_levels(self, levels):
        """Feed audio levels to the waveform."""
        self._waveform.set_audio_levels(levels)

    def clear_transcript(self):
        """Clear the transcript."""
        for widget in self._transcript.winfo_children():
            widget.destroy()
        self._empty_transcript = ctk.CTkLabel(
            self._transcript,
            text="Voice transcript will appear here...",
            font=("Segoe UI", 12),
            text_color=COLORS["text_tertiary"],
        )
        self._empty_transcript.pack(pady=SPACING["xl"])
