"""
Files Page — Desktop File Browser & Quick Open
==============================================
Browse local project files, output snapshots, and open directories.
"""

import os
import customtkinter as ctk
from bujji.config import PROJECT_ROOT, OUTPUT_DIR
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard
from bujji.automation.app_launcher import open_file_explorer


class FilesPage(ctk.CTkFrame):
    """
    Files browser & project assets view page.
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
            text="📁  Files & Storage",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Access local project files, saved camera snapshots, and output documents",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Quick Actions
        actions_card = GlassCard(self._scroll)
        actions_card.pack(fill="x", pady=(0, SPACING["xl"]))

        row = ctk.CTkFrame(actions_card.content, fg_color="transparent")
        row.pack(fill="x")

        open_exp_btn = ctk.CTkButton(
            row,
            text="📂 Open File Explorer",
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent_purple"],
            hover_color=COLORS["accent_purple_hover"],
            height=40,
            command=lambda: open_file_explorer(str(PROJECT_ROOT)),
        )
        open_exp_btn.pack(side="left", padx=(0, 8))

        # File List Card
        files_card = GlassCard(self._scroll, title="📄 Project Directory Files")
        files_card.pack(fill="x")

        self.files_container = ctk.CTkFrame(files_card.content, fg_color="transparent")
        self.files_container.pack(fill="x", pady=(4, 0))

        self.load_files()

    def load_files(self):
        for w in self.files_container.winfo_children():
            w.destroy()

        try:
            items = os.listdir(PROJECT_ROOT)
            for item in items[:20]:
                if item.startswith("."):
                    continue

                item_path = PROJECT_ROOT / item
                is_dir = item_path.is_dir()
                icon = "📁" if is_dir else "📄"

                row = ctk.CTkFrame(self.files_container, fg_color="transparent")
                row.pack(fill="x", pady=2)

                ctk.CTkLabel(
                    row,
                    text=f"{icon}  {item}",
                    font=("Segoe UI", 12),
                    text_color=COLORS["text_primary"],
                    anchor="w",
                ).pack(side="left")
        except Exception as e:
            ctk.CTkLabel(
                self.files_container,
                text=f"Error listing files: {e}",
                font=("Segoe UI", 12),
                text_color=COLORS["error"],
            ).pack()
