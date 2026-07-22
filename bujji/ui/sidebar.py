"""
Sidebar — Navigation sidebar for BUJJI AI
============================================
Left-side navigation with icons, labels, active state highlighting,
hover animations, and BUJJI branding.
"""

import customtkinter as ctk
from bujji.ui.theme import COLORS, FONTS, RADIUS, SPACING, SIDEBAR_ITEMS


class SidebarItem(ctk.CTkFrame):
    """A single clickable sidebar navigation item."""

    def __init__(self, master, icon, label, key, on_click=None, **kwargs):
        super().__init__(master, fg_color="transparent", cursor="hand2", **kwargs)

        self._key = key
        self._on_click = on_click
        self._is_active = False

        # Layout
        self.configure(height=44)

        # Active indicator bar (left edge)
        self._indicator = ctk.CTkFrame(
            self,
            width=3,
            height=28,
            fg_color="transparent",
            corner_radius=2,
        )
        self._indicator.place(x=0, rely=0.5, anchor="w")

        # Icon
        self._icon = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI", 18),
            width=32,
            anchor="center",
        )
        self._icon.place(x=20, rely=0.5, anchor="w")

        # Label
        self._label = ctk.CTkLabel(
            self,
            text=label,
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        self._label.place(x=58, rely=0.5, anchor="w")

        # Bind hover & click to all child widgets
        for widget in [self, self._icon, self._label]:
            widget.bind("<Button-1>", self._handle_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def set_active(self, active=True):
        self._is_active = active
        if active:
            self.configure(fg_color=COLORS["bg_sidebar_active"])
            self._indicator.configure(fg_color=COLORS["accent_purple"])
            self._label.configure(text_color=COLORS["text_primary"])
        else:
            self.configure(fg_color="transparent")
            self._indicator.configure(fg_color="transparent")
            self._label.configure(text_color=COLORS["text_secondary"])

    def _handle_click(self, event=None):
        if self._on_click:
            self._on_click(self._key)

    def _on_enter(self, event=None):
        if not self._is_active:
            self.configure(fg_color=COLORS["bg_sidebar_hover"])
            self._label.configure(text_color=COLORS["text_primary"])

    def _on_leave(self, event=None):
        if not self._is_active:
            self.configure(fg_color="transparent")
            self._label.configure(text_color=COLORS["text_secondary"])


class Sidebar(ctk.CTkFrame):
    """
    Navigation sidebar with:
    - User greeting at top
    - Navigation items with icons
    - Active state tracking
    - Hover animations
    - BUJJI branding at bottom
    """

    def __init__(self, master, user_name="Gouthami", on_navigate=None, **kwargs):
        super().__init__(
            master,
            width=240,
            fg_color=COLORS["bg_sidebar"],
            corner_radius=0,
            border_width=1,
            border_color=COLORS["border"],
            **kwargs,
        )
        self.pack_propagate(False)

        self._on_navigate = on_navigate
        self._items = {}
        self._active_key = "home"

        # ─── Header: User Info ────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=SPACING["lg"], pady=(SPACING["xl"], SPACING["md"]))

        # Avatar circle
        avatar = ctk.CTkLabel(
            header,
            text="👩‍💻",
            font=("Segoe UI", 28),
            width=48,
            height=48,
            fg_color=COLORS["bg_card"],
            corner_radius=24,
        )
        avatar.pack(anchor="w")

        # Name
        ctk.CTkLabel(
            header,
            text=f"Hi, {user_name}!",
            font=("Segoe UI", 15, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x", pady=(8, 0))

        # Status
        ctk.CTkLabel(
            header,
            text="● Online",
            font=("Segoe UI", 11),
            text_color=COLORS["success"],
            anchor="w",
        ).pack(fill="x")

        # ─── Separator ────────────────────────────────────────────────────
        sep = ctk.CTkFrame(self, height=1, fg_color=COLORS["border"])
        sep.pack(fill="x", padx=SPACING["lg"], pady=(SPACING["sm"], SPACING["md"]))

        # ─── Navigation Items ─────────────────────────────────────────────
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=SPACING["sm"])

        for item_data in SIDEBAR_ITEMS:
            item = SidebarItem(
                nav_frame,
                icon=item_data["icon"],
                label=item_data["label"],
                key=item_data["key"],
                on_click=self._navigate,
            )
            item.pack(fill="x", pady=1)
            self._items[item_data["key"]] = item

        # Set initial active
        self._items["home"].set_active(True)

        # ─── Footer: BUJJI Branding ───────────────────────────────────────
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=SPACING["lg"], pady=SPACING["lg"])

        sep2 = ctk.CTkFrame(footer, height=1, fg_color=COLORS["border"])
        sep2.pack(fill="x", pady=(0, SPACING["md"]))

        ctk.CTkLabel(
            footer,
            text="BUJJI AI",
            font=("Segoe UI Black", 14, "bold"),
            text_color=COLORS["accent_purple"],
            anchor="center",
        ).pack()

        ctk.CTkLabel(
            footer,
            text="v2.0.0",
            font=("Segoe UI", 10),
            text_color=COLORS["text_tertiary"],
            anchor="center",
        ).pack()

    def _navigate(self, key):
        """Handle navigation item click."""
        # Deactivate current
        if self._active_key in self._items:
            self._items[self._active_key].set_active(False)

        # Activate new
        self._active_key = key
        if key in self._items:
            self._items[key].set_active(True)

        # Notify parent
        if self._on_navigate:
            self._on_navigate(key)

    def set_active(self, key):
        """Programmatically set the active sidebar item without triggering callback."""
        if self._active_key == key:
            return
        if self._active_key in self._items:
            self._items[self._active_key].set_active(False)
        self._active_key = key
        if key in self._items:
            self._items[key].set_active(True)
