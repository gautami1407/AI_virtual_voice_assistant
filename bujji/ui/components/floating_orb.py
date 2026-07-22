"""
Floating Orb — Floating microphone button overlay
===================================================
A circular, pulsing microphone button that floats over the content.
Similar to Siri orb or Windows Copilot button.
"""

import math
import customtkinter as ctk
from bujji.ui.theme import COLORS, ANIMATION


class FloatingOrb(ctk.CTkFrame):
    """
    A floating, glowing microphone orb that can be placed anywhere.
    Pulses when idle, glows brighter when active (listening).
    """

    def __init__(self, master, size=64, on_click=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._size = size
        self._canvas_size = size + 30  # Space for glow
        self._on_click = on_click
        self._active = False
        self._phase = 0.0
        self._animating = True

        # Canvas
        self.canvas = ctk.CTkCanvas(
            self,
            width=self._canvas_size,
            height=self._canvas_size,
            bg=COLORS["bg_primary"],
            highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._handle_click)

        # Status label
        self._status = ctk.CTkLabel(
            self,
            text="Click to speak",
            font=("Segoe UI", 10),
            text_color=COLORS["text_secondary"],
        )
        self._status.pack(pady=(2, 0))

        self._animate()

    def set_active(self, active=True):
        """Toggle listening state."""
        self._active = active
        if active:
            self._status.configure(text="Listening...", text_color=COLORS["accent_neon"])
        else:
            self._status.configure(text="Click to speak", text_color=COLORS["text_secondary"])

    def set_status(self, text):
        """Update the status text below the orb."""
        self._status.configure(text=text)

    def _handle_click(self, event=None):
        if self._on_click:
            self._on_click()

    def _animate(self):
        if not self._animating:
            return

        self.canvas.delete("all")
        cx = self._canvas_size / 2
        cy = self._canvas_size / 2

        pulse = (math.sin(self._phase) + 1) / 2  # 0..1

        if self._active:
            # Active: brighter glow, faster pulse
            glow_color = COLORS["accent_neon"]
            ring_color = COLORS["accent_cyan"]
            bg_color = "#0D3B3B"
            mic_color = COLORS["accent_neon"]
            glow_radius = self._size / 2 + 8 + pulse * 10
        else:
            # Idle: subtle purple glow
            glow_color = COLORS["accent_purple"]
            ring_color = COLORS["accent_purple"]
            bg_color = COLORS["bg_secondary"]
            mic_color = COLORS["accent_purple"]
            glow_radius = self._size / 2 + 4 + pulse * 5

        # Outer glow rings
        for i in range(3, 0, -1):
            r = glow_radius + i * 5
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill="", outline=ring_color,
                width=1,
            )

        # Main circle
        r = self._size / 2
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=bg_color,
            outline=ring_color,
            width=2,
        )

        # Microphone icon (text emoji)
        self.canvas.create_text(
            cx, cy,
            text="🎤",
            font=("Segoe UI", int(self._size * 0.35)),
        )

        self._phase += 0.08 if self._active else 0.04
        self.after(ANIMATION["waveform"], self._animate)

    def stop(self):
        self._animating = False

    def start(self):
        if not self._animating:
            self._animating = True
            self._animate()
