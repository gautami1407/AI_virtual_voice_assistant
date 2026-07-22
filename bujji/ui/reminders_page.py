"""
Reminders Page — Tasks, Todo List & Reminders Management
========================================================
Create, list, and manage reminders and todo items.
"""

import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard


class RemindersPage(ctk.CTkFrame):
    """
    Reminders and Todo List page.
    """

    def __init__(self, master, db_manager=None, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)
        self.db = db_manager

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
            text="🗓  Reminders & Tasks",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Manage your daily todos, schedule reminders, and track productivity goals",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Add Task Bar
        add_card = GlassCard(self._scroll)
        add_card.pack(fill="x", pady=(0, SPACING["xl"]))

        row = ctk.CTkFrame(add_card.content, fg_color="transparent")
        row.pack(fill="x")
        row.columnconfigure(0, weight=1)

        self.task_entry = ctk.CTkEntry(
            row,
            placeholder_text="Add a new reminder or todo item...",
            font=("Segoe UI", 13),
            fg_color=COLORS["bg_input"],
            height=40,
        )
        self.task_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        btn = ctk.CTkButton(
            row,
            text="＋ Add Task",
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent_purple"],
            hover_color=COLORS["accent_purple_hover"],
            height=40,
            command=self.add_task,
        )
        btn.grid(row=0, column=1)

        # Task List Container
        self.task_container = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self.task_container.pack(fill="x")

        self.tasks = []
        self.render_tasks()

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return
        self.task_entry.delete(0, "end")
        self.tasks.append({"text": text, "done": False})
        self.render_tasks()

    def toggle_task(self, idx):
        if 0 <= idx < len(self.tasks):
            self.tasks[idx]["done"] = not self.tasks[idx]["done"]
            self.render_tasks()

    def delete_task(self, idx):
        if 0 <= idx < len(self.tasks):
            self.tasks.pop(idx)
            self.render_tasks()

    def render_tasks(self):
        for w in self.task_container.winfo_children():
            w.destroy()

        if not self.tasks:
            ctk.CTkLabel(
                self.task_container,
                text="No reminders added yet.\nType a task above to get started! 🎯",
                font=("Segoe UI", 13),
                text_color=COLORS["text_tertiary"],
                justify="center",
            ).pack(pady=SPACING["xl"])
            return

        for idx, task in enumerate(self.tasks):
            card = GlassCard(self.task_container)
            card.pack(fill="x", pady=4)

            row = ctk.CTkFrame(card.content, fg_color="transparent")
            row.pack(fill="x")
            row.columnconfigure(1, weight=1)

            check = ctk.CTkCheckBox(
                row,
                text="",
                width=24,
                command=lambda i=idx: self.toggle_task(i),
            )
            if task["done"]:
                check.select()
            check.grid(row=0, column=0, padx=(0, 8))

            text_color = COLORS["text_tertiary"] if task["done"] else COLORS["text_primary"]
            lbl = ctk.CTkLabel(
                row,
                text=task["text"],
                font=("Segoe UI", 13, "overstrike" if task["done"] else "normal"),
                text_color=text_color,
                anchor="w",
            )
            lbl.grid(row=0, column=1, sticky="w")

            del_btn = ctk.CTkButton(
                row,
                text="🗑",
                width=30,
                height=28,
                fg_color="transparent",
                hover_color=COLORS["error"],
                command=lambda i=idx: self.delete_task(i),
            )
            del_btn.grid(row=0, column=2)
