"""
Productivity Page — Focus Timer, QR Code, Password Gen & Document AI
====================================================================
Comprehensive productivity suite view page.
"""

from PIL import Image
import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard
from bujji.productivity.timer import PomodoroTimer
from bujji.productivity.tools import generate_password, generate_qr_code
from bujji.ai.document_ai import extract_pdf_text


class ProductivityPage(ctk.CTkFrame):
    """
    Productivity Suite view page.
    """

    def __init__(self, master, app_controller=None, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)
        self.app = app_controller

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
            text="⚡  Productivity & AI Tools",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Pomodoro focus timer, secure password generator, QR code creator, and PDF Document AI",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Grid layout (2 Columns)
        grid = ctk.CTkFrame(self._scroll, fg_color="transparent")
        grid.pack(fill="x")
        grid.columnconfigure((0, 1), weight=1)

        # 1. Pomodoro Focus Timer Card
        pomo_card = GlassCard(grid, title="⏱  Pomodoro Focus Timer")
        pomo_card.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="nsew")

        self.pomo_time_lbl = ctk.CTkLabel(
            pomo_card.content,
            text="25:00",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLORS["accent_purple"],
        )
        self.pomo_time_lbl.pack(pady=8)

        pomo_btns = ctk.CTkFrame(pomo_card.content, fg_color="transparent")
        pomo_btns.pack()

        self.pomo_timer = PomodoroTimer(
            on_tick=lambda t, m: self.after(0, lambda: self.pomo_time_lbl.configure(text=t)),
            on_finish=lambda m: self.after(0, lambda: self.pomo_time_lbl.configure(text="Done! 🎉")),
        )

        start_btn = ctk.CTkButton(
            pomo_btns,
            text="▶ Start",
            width=70,
            fg_color=COLORS["accent_purple"],
            command=self.pomo_timer.start,
        )
        start_btn.pack(side="left", padx=4)

        pause_btn = ctk.CTkButton(
            pomo_btns,
            text="⏸ Pause",
            width=70,
            fg_color=COLORS["bg_card"],
            command=self.pomo_timer.pause,
        )
        pause_btn.pack(side="left", padx=4)

        reset_btn = ctk.CTkButton(
            pomo_btns,
            text="🔄 Reset",
            width=70,
            fg_color=COLORS["bg_card"],
            command=self.reset_pomo,
        )
        reset_btn.pack(side="left", padx=4)

        # 2. Password Generator Card
        pass_card = GlassCard(grid, title="🔐 Password Generator")
        pass_card.grid(row=0, column=1, padx=(8, 0), pady=8, sticky="nsew")

        self.pass_entry = ctk.CTkEntry(
            pass_card.content,
            font=("Cascadia Code", 13, "bold"),
            fg_color=COLORS["bg_input"],
            height=38,
        )
        self.pass_entry.pack(fill="x", pady=(8, 8))

        gen_pass_btn = ctk.CTkButton(
            pass_card.content,
            text="⚡ Generate Secure Password",
            font=("Segoe UI", 12, "bold"),
            fg_color=COLORS["accent_cyan"],
            command=self.gen_pass,
        )
        gen_pass_btn.pack(anchor="w")

        # 3. QR Code Generator Card
        qr_card = GlassCard(self._scroll, title="📱 QR Code Generator")
        qr_card.pack(fill="x", pady=8)

        qr_row = ctk.CTkFrame(qr_card.content, fg_color="transparent")
        qr_row.pack(fill="x")
        qr_row.columnconfigure(0, weight=1)

        self.qr_input = ctk.CTkEntry(
            qr_row,
            placeholder_text="Enter website URL or text to create QR code...",
            height=38,
        )
        self.qr_input.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        make_qr_btn = ctk.CTkButton(
            qr_row,
            text="Generate QR",
            font=("Segoe UI", 12, "bold"),
            fg_color=COLORS["accent_neon"],
            text_color="#000000",
            command=self.make_qr,
        )
        make_qr_btn.grid(row=0, column=1)

        self.qr_img_lbl = ctk.CTkLabel(
            qr_card.content,
            text="",
        )
        self.qr_img_lbl.pack(pady=8)

        # 4. Document AI / PDF Reader Card
        doc_card = GlassCard(self._scroll, title="📄 Document AI — PDF Text Extractor")
        doc_card.pack(fill="x", pady=8)

        doc_row = ctk.CTkFrame(doc_card.content, fg_color="transparent")
        doc_row.pack(fill="x")
        doc_row.columnconfigure(0, weight=1)

        self.pdf_entry = ctk.CTkEntry(
            doc_row,
            placeholder_text="Enter absolute path to PDF file (e.g. C:/Users/.../document.pdf)...",
            height=38,
        )
        self.pdf_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        read_pdf_btn = ctk.CTkButton(
            doc_row,
            text="Extract & Summarize",
            font=("Segoe UI", 12, "bold"),
            fg_color=COLORS["accent_purple"],
            command=self.read_pdf,
        )
        read_pdf_btn.grid(row=0, column=1)

        self.pdf_out = ctk.CTkTextbox(
            doc_card.content,
            height=150,
            font=("Segoe UI", 12),
            fg_color=COLORS["bg_input"],
        )
        self.pdf_out.pack(fill="x", pady=(8, 0))

    def reset_pomo(self):
        self.pomo_timer.reset()
        self.pomo_time_lbl.configure(text="25:00")

    def gen_pass(self):
        pw = generate_password(16)
        self.pass_entry.delete(0, "end")
        self.pass_entry.insert(0, pw)

    def make_qr(self):
        txt = self.qr_input.get().strip()
        if not txt:
            return
        img_path = generate_qr_code(txt)
        if img_path:
            pil = Image.open(img_path)
            pil.thumbnail((150, 150))
            ctk_img = ctk.CTkImage(light_image=pil, dark_image=pil, size=pil.size)
            self.qr_img_lbl.configure(image=ctk_img, text="")

    def read_pdf(self):
        path = self.pdf_entry.get().strip()
        if not path:
            return
        text = extract_pdf_text(path)
        self.pdf_out.delete("1.0", "end")
        self.pdf_out.insert("1.0", text[:2000])

        # If app controller available, send to AI for auto-summary!
        if self.app and "Error" not in text and "not installed" not in text:
            prompt = f"Summarize key points from this document:\n\n{text[:1500]}"
            self.app.process_chat_message(prompt)
            self.app.window.show_page("chat")
