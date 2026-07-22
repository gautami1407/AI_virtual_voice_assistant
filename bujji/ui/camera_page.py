"""
Camera Page — Web camera preview & photo snapshot tool
======================================================
Captures camera frames, displays preview, and saves photos.
"""

import threading
import cv2
from PIL import Image
import customtkinter as ctk
from bujji.config import OUTPUT_DIR
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard


class CameraPage(ctk.CTkFrame):
    """
    Camera capture view page.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)

        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["scrollbar_thumb"],
        )
        self._scroll.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["lg"])

        # Header
        header = ctk.CTkFrame(self._scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING["xl"]))

        ctk.CTkLabel(
            header,
            text="📷  Camera Snapshot",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Capture photo snapshots from your webcam",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Controls Card
        card = GlassCard(self._scroll)
        card.pack(fill="x", pady=(0, SPACING["xl"]))

        btn_row = ctk.CTkFrame(card.content, fg_color="transparent")
        btn_row.pack(fill="x")

        snap_btn = ctk.CTkButton(
            btn_row,
            text="📸 Capture Snapshot",
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent_purple"],
            hover_color=COLORS["accent_purple_hover"],
            height=40,
            command=self.take_photo,
        )
        snap_btn.pack(side="left", padx=(0, 8))

        self.status_lbl = ctk.CTkLabel(
            btn_row,
            text="Click 'Capture Snapshot' to take a photo",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self.status_lbl.pack(side="left", padx=8)

        # Image Display Label
        self.img_card = GlassCard(self._scroll, title="Preview")
        self.img_card.pack(fill="x")

        self.preview_label = ctk.CTkLabel(
            self.img_card.content,
            text="[ No photo taken yet ]",
            font=("Segoe UI", 14),
            text_color=COLORS["text_tertiary"],
            height=300,
        )
        self.preview_label.pack(fill="both", expand=True)

    def take_photo(self):
        self.status_lbl.configure(text="Opening camera...")

        def _capture():
            try:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    self.after(0, lambda: self.status_lbl.configure(text="❌ Error: Webcam not accessible."))
                    return

                ret, frame = cap.read()
                cap.release()

                if ret:
                    # Save image
                    out_path = OUTPUT_DIR / "camera_snapshot.png"
                    cv2.imwrite(str(out_path), frame)

                    # Convert BGR to RGB for CTkImage / PIL
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(rgb)

                    # Resize preview
                    pil_img.thumbnail((500, 350))
                    ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)

                    def _update():
                        self.preview_label.configure(image=ctk_img, text="")
                        self.status_lbl.configure(text=f"✅ Saved snapshot to {out_path.name}")

                    self.after(0, _update)
                else:
                    self.after(0, lambda: self.status_lbl.configure(text="❌ Failed to read camera frame."))
            except Exception as e:
                self.after(0, lambda: self.status_lbl.configure(text=f"❌ Error: {e}"))

        threading.Thread(target=_capture, daemon=True).start()
