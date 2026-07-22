"""
Waveform — Voice waveform visualization
=========================================
Canvas-based animated audio waveform that responds to audio levels.
"""

import math
import random
import customtkinter as ctk
from bujji.ui.theme import COLORS, ANIMATION


class WaveformVisualizer(ctk.CTkFrame):
    """
    Animated voice waveform visualization using canvas.
    Shows bars that react to audio input or idle animation.
    """

    def __init__(self, master, width=400, height=80, bar_count=40, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._width = width
        self._height = height
        self._bar_count = bar_count
        self._animating = False
        self._active = False
        self._phase = 0.0
        self._audio_levels = [0.0] * bar_count

        # Canvas
        self.canvas = ctk.CTkCanvas(
            self,
            width=width,
            height=height,
            bg=COLORS["bg_primary"],
            highlightthickness=0,
        )
        self.canvas.pack()

    def set_active(self, active=True):
        """Switch between active (listening) and idle state."""
        self._active = active
        if active and not self._animating:
            self.start()

    def set_audio_levels(self, levels):
        """Feed real audio amplitude data (list of 0.0–1.0 floats)."""
        # Resample to match bar count
        if len(levels) != self._bar_count:
            step = max(1, len(levels) // self._bar_count)
            self._audio_levels = [levels[i * step] if i * step < len(levels) else 0
                                  for i in range(self._bar_count)]
        else:
            self._audio_levels = levels

    def start(self):
        """Start the waveform animation."""
        self._animating = True
        self._animate()

    def stop(self):
        """Stop the animation and show flat bars."""
        self._animating = False
        self._active = False
        self.canvas.delete("all")
        self._draw_idle()

    def _animate(self):
        if not self._animating:
            return

        self.canvas.delete("all")

        bar_width = self._width / self._bar_count
        gap = 2
        center_y = self._height / 2

        for i in range(self._bar_count):
            if self._active:
                # Active: Use audio levels or simulated active wave
                if sum(self._audio_levels) > 0.1:
                    amp = self._audio_levels[i]
                else:
                    # Simulated active wave
                    amp = (
                        0.3
                        + 0.4 * abs(math.sin(self._phase + i * 0.3))
                        + 0.2 * abs(math.sin(self._phase * 1.7 + i * 0.5))
                        + random.uniform(0, 0.15)
                    )
            else:
                # Idle: Gentle sine wave
                amp = 0.08 + 0.06 * abs(math.sin(self._phase * 0.5 + i * 0.2))

            bar_height = max(3, amp * (self._height * 0.8))
            x1 = i * bar_width + gap / 2
            x2 = (i + 1) * bar_width - gap / 2
            y1 = center_y - bar_height / 2
            y2 = center_y + bar_height / 2

            # Color: gradient from purple to cyan based on position
            if self._active:
                # Interpolate between purple and cyan
                t = i / max(1, self._bar_count - 1)
                r = int(139 * (1 - t) + 6 * t)
                g = int(92 * (1 - t) + 182 * t)
                b = int(246 * (1 - t) + 212 * t)
                color = f"#{r:02x}{g:02x}{b:02x}"
            else:
                color = COLORS["waveform_idle"]

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="",
                # Rounded corners aren't supported in canvas rects,
                # but the small size makes them look fine
            )

        self._phase += 0.12
        self.after(ANIMATION["waveform"], self._animate)

    def _draw_idle(self):
        """Draw static idle bars."""
        bar_width = self._width / self._bar_count
        gap = 2
        center_y = self._height / 2

        for i in range(self._bar_count):
            bar_height = 4
            x1 = i * bar_width + gap / 2
            x2 = (i + 1) * bar_width - gap / 2
            y1 = center_y - bar_height / 2
            y2 = center_y + bar_height / 2

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=COLORS["waveform_idle"],
                outline="",
            )
