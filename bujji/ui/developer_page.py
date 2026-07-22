"""
Developer Page — Developer Tools, Prompt Templates, GitHub & LeetCode Dashboard
================================================================================
Tailored tools for software engineering candidates: code generation templates,
GitHub profile statistics, and LeetCode problem trackers.
"""

import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard


class DeveloperPage(ctk.CTkFrame):
    """
    Developer Mode & Resume Showcase view page.
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
            text="💻  Developer Hub & Resume Showcase",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="AI code generation templates, Git/Docker cheat-sheets, GitHub stats, and LeetCode tracker",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Dashboard Grid (2 columns)
        grid = ctk.CTkFrame(self._scroll, fg_color="transparent")
        grid.pack(fill="x", pady=(0, SPACING["xl"]))
        grid.columnconfigure((0, 1), weight=1)

        # 1. GitHub Profile Showcase Card
        gh_card = GlassCard(grid, title="🐙  GitHub Portfolio Dashboard")
        gh_card.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="nsew")

        gh_stats = [
            ("Repositories", "12 Active"),
            ("Commits (This Month)", "48 Commits"),
            ("Open PRs / Issues", "3 PRs"),
        ]
        for label, val in gh_stats:
            r = ctk.CTkFrame(gh_card.content, fg_color="transparent")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=label, font=("Segoe UI", 12), text_color=COLORS["text_secondary"]).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Segoe UI", 12, "bold"), text_color=COLORS["accent_purple"]).pack(side="right")

        # 2. LeetCode Tracker Card
        lc_card = GlassCard(grid, title="🧩  LeetCode Problem Tracker")
        lc_card.grid(row=0, column=1, padx=(8, 0), pady=8, sticky="nsew")

        lc_stats = [
            ("Solved Problems", "145 Solved"),
            ("Daily Streak", "14 Days 🔥"),
            ("Global Ranking", "Top 15%"),
        ]
        for label, val in lc_stats:
            r = ctk.CTkFrame(lc_card.content, fg_color="transparent")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=label, font=("Segoe UI", 12), text_color=COLORS["text_secondary"]).pack(side="left")
            ctk.CTkLabel(r, text=val, font=("Segoe UI", 12, "bold"), text_color=COLORS["accent_cyan"]).pack(side="right")

        # 3. AI Code Assistant Prompt Shortcuts
        prompts_card = GlassCard(self._scroll, title="⚡  AI Code Assistant Prompt Templates")
        prompts_card.pack(fill="x", pady=8)

        templates = [
            ("🐍 Generate Python Class", "Write a clean Python class with type hints and docstrings for "),
            ("🗄️ Write SQL Query", "Write an optimized SQL query with JOINs and window functions to "),
            ("🌐 Generate HTML/CSS Component", "Create a modern responsive HTML/CSS UI component for "),
            ("🐛 Debug Code", "Analyze this code for bugs, race conditions, and edge cases:\n"),
            ("🐙 Git Commands", "Explain the exact Git commands step-by-step to "),
            ("🐳 Docker Reference", "Write a Dockerfile and docker-compose.yml file for "),
        ]

        t_grid = ctk.CTkFrame(prompts_card.content, fg_color="transparent")
        t_grid.pack(fill="x", pady=(4, 0))
        t_grid.columnconfigure((0, 1), weight=1)

        for idx, (title, prompt_prefix) in enumerate(templates):
            row = idx // 2
            col = idx % 2
            btn = ctk.CTkButton(
                t_grid,
                text=title,
                font=("Segoe UI", 12, "bold"),
                fg_color=COLORS["bg_card"],
                hover_color=COLORS["accent_purple"],
                height=36,
                command=lambda p=prompt_prefix: self.use_template(p),
            )
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

    def use_template(self, prefix):
        if self.app:
            self.app.window.chat_page._send_suggestion(prefix)
            self.app.window.show_page("chat")
