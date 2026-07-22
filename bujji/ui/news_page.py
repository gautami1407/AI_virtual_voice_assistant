"""
News Page — AI & Technology News Dashboard
==========================================
Fetches latest headlines from RSS feeds with category filters and open-in-browser links.
"""

import threading
import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard
from bujji.automation.browser_control import fetch_news_rss, open_url


class NewsPage(ctk.CTkFrame):
    """
    News Dashboard view page.
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
            text="📰  News Dashboard",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Stay updated with real-time headlines across Technology, AI, Cloud, and World news",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Categories filter bar
        cat_card = GlassCard(self._scroll)
        cat_card.pack(fill="x", pady=(0, SPACING["xl"]))

        cat_row = ctk.CTkFrame(cat_card.content, fg_color="transparent")
        cat_row.pack(fill="x")

        categories = ["Technology", "Artificial Intelligence", "India", "World"]
        for cat in categories:
            btn = ctk.CTkButton(
                cat_row,
                text=cat,
                font=("Segoe UI", 12, "bold"),
                fg_color=COLORS["bg_card"],
                hover_color=COLORS["accent_purple"],
                command=lambda c=cat: self.load_news(c),
            )
            btn.pack(side="left", padx=4)

        # Articles container
        self.articles_container = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self.articles_container.pack(fill="x")

        # Load initial news
        self.load_news("Technology")

    def load_news(self, category):
        for w in self.articles_container.winfo_children():
            w.destroy()

        loading_lbl = ctk.CTkLabel(
            self.articles_container,
            text=f"Loading {category} headlines...",
            font=("Segoe UI", 14),
            text_color=COLORS["text_tertiary"],
        )
        loading_lbl.pack(pady=SPACING["xl"])

        def _fetch():
            articles = fetch_news_rss(category)

            def _update_ui():
                loading_lbl.destroy()
                if not articles:
                    ctk.CTkLabel(
                        self.articles_container,
                        text="No articles found.",
                        font=("Segoe UI", 13),
                        text_color=COLORS["text_tertiary"],
                    ).pack(pady=SPACING["xl"])
                    return

                for article in articles:
                    card = GlassCard(self.articles_container)
                    card.pack(fill="x", pady=4)

                    title_lbl = ctk.CTkLabel(
                        card.content,
                        text=article["title"],
                        font=("Segoe UI", 13, "bold"),
                        text_color=COLORS["text_primary"],
                        anchor="w",
                        justify="left",
                        wraplength=650,
                    )
                    title_lbl.pack(fill="x")

                    meta_row = ctk.CTkFrame(card.content, fg_color="transparent")
                    meta_row.pack(fill="x", pady=(4, 0))

                    ctk.CTkLabel(
                        meta_row,
                        text=f"🕒 {article['pub_date']}",
                        font=("Segoe UI", 11),
                        text_color=COLORS["text_secondary"],
                    ).pack(side="left")

                    read_btn = ctk.CTkButton(
                        meta_row,
                        text="Read Full Article 🔗",
                        font=("Segoe UI", 11),
                        width=120,
                        height=24,
                        fg_color=COLORS["accent_purple"],
                        command=lambda link=article["link"]: open_url(link),
                    )
            try:
                if self.winfo_exists():
                    self.after(0, _update_ui)
            except Exception:
                pass

        threading.Thread(target=_fetch, daemon=True).start()
