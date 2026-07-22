"""
Animated Logo — Pulsing BUJJI AI logo with glow effect
=======================================================
Canvas-based logo with a smooth pulsing glow animation.
"""

import math
import customtkinter as ctk
from bujji.ui.theme import COLORS, ANIMATION


class AnimatedLogo(ctk.CTkFrame):
    """
    A pulsing 'BUJJI AI' text logo rendered on a canvas with a
    smooth, glowing animation cycle.
    """

    def __init__(self, master, size=120, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._size = size
        self._canvas_size = size + 60  # Extra space for glow
        self._phase = 0.0
        self._animating = True

        # Canvas for the logo
        self.canvas = ctk.CTkCanvas(
            self,
            width=self._canvas_size,
            height=self._canvas_size,
            bg=COLORS["bg_primary"],
            highlightthickness=0,
        )
        self.canvas.pack()

        # Subtitle
        self.subtitle = ctk.CTkLabel(
            self,
            text="Your Intelligent Companion",
            font=("Segoe UI", 11),
            text_color=COLORS["text_secondary"],
        )
        self.subtitle.pack(pady=(4, 0))

        self._animate()

    def _animate(self):
        if not self._animating:
            return

        self.canvas.delete("all")
        cx = self._canvas_size / 2
        cy = self._canvas_size / 2

        # Pulsing glow — sine wave from 0.3 to 1.0 opacity
        pulse = (math.sin(self._phase) + 1) / 2  # 0..1
        glow_radius = self._size / 2 + 10 + pulse * 15

        # Draw concentric glow rings (outer to inner)
        for i in range(5, 0, -1):
            r = glow_radius + i * 6
            # Fade alpha with distance
            alpha_hex = format(int(20 + pulse * 30 - i * 5), "02x")
            color = f"#8B5C{alpha_hex}"
            try:
                self.canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    fill="", outline=COLORS["accent_purple"],
                    width=1,
                )
            except Exception:
                pass

        # Inner filled circle
        inner_r = self._size / 2 - 5 + pulse * 3
        self.canvas.create_oval(
            cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r,
            fill=COLORS["bg_secondary"],
            outline=COLORS["accent_purple"],
            width=2,
        )

        # BUJJI text
        self.canvas.create_text(
            cx, cy - 8,
            text="BUJJI",
            fill=COLORS["accent_purple"],
            font=("Segoe UI Black", 22, "bold"),
        )

        # AI text
        self.canvas.create_text(
            cx, cy + 18,
            text="AI",
            fill=COLORS["accent_cyan"],
            font=("Segoe UI", 14, "bold"),
        )

        # Small dot pulse indicator at bottom
        dot_r = 3 + pulse * 2
        dot_y = cy + inner_r - 12
        self.canvas.create_oval(
            cx - dot_r, dot_y - dot_r, cx + dot_r, dot_y + dot_r,
            fill=COLORS["accent_neon"],
            outline="",
        )

        self._phase += 0.06
        self.after(ANIMATION["waveform"], self._animate)

    def stop(self):
        self._animating = False

    def start(self):
        if not self._animating:
            self._animating = True
            self._animate()
