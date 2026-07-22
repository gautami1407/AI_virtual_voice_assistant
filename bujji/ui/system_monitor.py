"""
System Monitor Page — Real-time CPU, RAM, Disk, Battery & Process Dashboard
===========================================================================
Displays live resource utilization graphs/bars, battery info, and active processes.
"""

import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard
from bujji.automation.system_control import get_system_stats, get_running_processes, system_action


class SystemMonitorPage(ctk.CTkFrame):
    """
    System Monitor Dashboard view page.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)

        # Main scroll container
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=COLORS["scrollbar_thumb"],
        )
        self._scroll.pack(fill="both", expand=True, padx=SPACING["xl"], pady=SPACING["lg"])

        # Page Header
        header = ctk.CTkFrame(self._scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING["xl"]))

        ctk.CTkLabel(
            header,
            text="📊  System Monitor",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Real-time CPU, Memory, Storage utilization and background process manager",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Metrics Cards Grid (2x2)
        metrics_grid = ctk.CTkFrame(self._scroll, fg_color="transparent")
        metrics_grid.pack(fill="x", pady=(0, SPACING["xl"]))
        metrics_grid.columnconfigure((0, 1), weight=1)

        # CPU Card
        self.cpu_card = GlassCard(metrics_grid, title="⚡ CPU Utilization")
        self.cpu_card.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="nsew")

        self.cpu_lbl = ctk.CTkLabel(
            self.cpu_card.content,
            text="0%",
            font=("Segoe UI Black", 28, "bold"),
            text_color=COLORS["accent_purple"],
        )
        self.cpu_lbl.pack(anchor="w")

        self.cpu_bar = ctk.CTkProgressBar(
            self.cpu_card.content,
            progress_color=COLORS["accent_purple"],
            fg_color=COLORS["bg_input"],
        )
        self.cpu_bar.pack(fill="x", pady=(8, 0))
        self.cpu_bar.set(0)

        # RAM Card
        self.ram_card = GlassCard(metrics_grid, title="🧠 RAM Usage")
        self.ram_card.grid(row=0, column=1, padx=(8, 0), pady=8, sticky="nsew")

        self.ram_lbl = ctk.CTkLabel(
            self.ram_card.content,
            text="0 / 0 GB",
            font=("Segoe UI Black", 24, "bold"),
            text_color=COLORS["accent_cyan"],
        )
        self.ram_lbl.pack(anchor="w")

        self.ram_bar = ctk.CTkProgressBar(
            self.ram_card.content,
            progress_color=COLORS["accent_cyan"],
            fg_color=COLORS["bg_input"],
        )
        self.ram_bar.pack(fill="x", pady=(8, 0))
        self.ram_bar.set(0)

        # Disk Card
        self.disk_card = GlassCard(metrics_grid, title="💾 Storage Space")
        self.disk_card.grid(row=1, column=0, padx=(0, 8), pady=8, sticky="nsew")

        self.disk_lbl = ctk.CTkLabel(
            self.disk_card.content,
            text="0 GB Free",
            font=("Segoe UI Black", 24, "bold"),
            text_color=COLORS["accent_neon"],
        )
        self.disk_lbl.pack(anchor="w")

        self.disk_bar = ctk.CTkProgressBar(
            self.disk_card.content,
            progress_color=COLORS["accent_neon"],
            fg_color=COLORS["bg_input"],
        )
        self.disk_bar.pack(fill="x", pady=(8, 0))
        self.disk_bar.set(0)

        # Battery Card
        self.bat_card = GlassCard(metrics_grid, title="🔋 Battery Status")
        self.bat_card.grid(row=1, column=1, padx=(8, 0), pady=8, sticky="nsew")

        self.bat_lbl = ctk.CTkLabel(
            self.bat_card.content,
            text="Checking...",
            font=("Segoe UI Black", 24, "bold"),
            text_color=COLORS["success"],
        )
        self.bat_lbl.pack(anchor="w")

        # System Actions Bar
        actions_card = GlassCard(self._scroll, title="⚙  Quick System Controls")
        actions_card.pack(fill="x", pady=(0, SPACING["xl"]))

        btn_row = ctk.CTkFrame(actions_card.content, fg_color="transparent")
        btn_row.pack(fill="x", pady=(8, 0))

        lock_btn = ctk.CTkButton(
            btn_row,
            text="🔒 Lock PC",
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_primary"],
            command=lambda: system_action("lock"),
        )
        lock_btn.pack(side="left", padx=(0, 8))

        # Process Manager Section
        proc_card = GlassCard(self._scroll, title="🔥 Top Active Processes (by RAM)")
        proc_card.pack(fill="x", pady=(0, SPACING["xl"]))

        self.proc_container = ctk.CTkFrame(proc_card.content, fg_color="transparent")
        self.proc_container.pack(fill="x", pady=(8, 0))

        self._update_loop()

    def _update_loop(self):
        """Periodically update system metrics and processes."""
        stats = get_system_stats()

        # Update CPU
        cpu = stats["cpu_percent"]
        self.cpu_lbl.configure(text=f"{cpu}%")
        self.cpu_bar.set(cpu / 100.0)

        # Update RAM
        ram_p = stats["ram_percent"]
        self.ram_lbl.configure(text=f"{stats['ram_used_gb']} GB ({ram_p}%)")
        self.ram_bar.set(ram_p / 100.0)

        # Update Disk
        disk_p = stats["disk_percent"]
        self.disk_lbl.configure(text=f"{stats['disk_free_gb']} GB Free ({disk_p}%)")
        self.disk_bar.set(disk_p / 100.0)

        # Update Battery
        bat = stats["battery"]
        bat_text = f"{bat['percent']}%" if bat["percent"] != "N/A" else "Desktop Mode"
        if bat["plugged"]:
            bat_text += " ⚡ (Charging)"
        self.bat_lbl.configure(text=bat_text)

        # Update Process Table
        for w in self.proc_container.winfo_children():
            w.destroy()

        procs = get_running_processes(limit=8)
        for p in procs:
            row = ctk.CTkFrame(self.proc_container, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(
                row, text=p['name'][:25], font=("Segoe UI", 12, "bold"),
                text_color=COLORS["text_primary"], width=180, anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=f"RAM: {p['memory']}%", font=("Segoe UI", 12),
                text_color=COLORS["accent_cyan"], width=100, anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=f"CPU: {p['cpu']}%", font=("Segoe UI", 12),
                text_color=COLORS["text_secondary"], width=100, anchor="w",
            ).pack(side="left")

        self.after(3000, self._update_loop)
