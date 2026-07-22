"""
Games Page — Mini Game Hub
==========================
CustomTkinter port of the mini-games (Guess Number, Rock Paper Scissors, Tic Tac Toe).
"""

import random
import customtkinter as ctk
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard


class GamesPage(ctk.CTkFrame):
    """
    Games Hub view page.
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
            text="🎮  BUJJI Game Hub",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Play quick interactive mini-games directly inside BUJJI AI",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Games Grid
        games_grid = ctk.CTkFrame(self._scroll, fg_color="transparent")
        games_grid.pack(fill="x")
        games_grid.columnconfigure((0, 1), weight=1)

        # 1. Rock Paper Scissors Card
        rps_card = GlassCard(games_grid, title="✊✌️✋ Rock Paper Scissors")
        rps_card.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="nsew")

        self.rps_status = ctk.CTkLabel(
            rps_card.content,
            text="Choose your move:",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self.rps_status.pack(pady=(4, 8))

        rps_btns = ctk.CTkFrame(rps_card.content, fg_color="transparent")
        rps_btns.pack()

        for move in ["Rock ✊", "Paper ✋", "Scissors ✌️"]:
            b = ctk.CTkButton(
                rps_btns,
                text=move,
                width=80,
                fg_color=COLORS["bg_card"],
                hover_color=COLORS["accent_purple"],
                command=lambda m=move.split()[0].lower(): self.play_rps(m),
            )
            b.pack(side="left", padx=4)

        # 2. Guess the Number Card
        guess_card = GlassCard(games_grid, title="🔢 Guess the Number")
        guess_card.grid(row=0, column=1, padx=(8, 0), pady=8, sticky="nsew")

        self.secret_num = random.randint(1, 100)
        self.attempts = 0

        self.guess_lbl = ctk.CTkLabel(
            guess_card.content,
            text="Guess a number between 1 and 100:",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self.guess_lbl.pack(pady=(4, 8))

        guess_row = ctk.CTkFrame(guess_card.content, fg_color="transparent")
        guess_row.pack()

        self.guess_entry = ctk.CTkEntry(guess_row, width=80, placeholder_text="Num...")
        self.guess_entry.pack(side="left", padx=(0, 4))

        sub_btn = ctk.CTkButton(
            guess_row,
            text="Submit",
            width=70,
            fg_color=COLORS["accent_cyan"],
            command=self.check_guess,
        )
        sub_btn.pack(side="left")

        # 3. Tic Tac Toe Card
        ttt_card = GlassCard(self._scroll, title="❌⭕ Tic Tac Toe")
        ttt_card.pack(fill="x", pady=8)

        self.ttt_status = ctk.CTkLabel(
            ttt_card.content,
            text="Player X's turn",
            font=("Segoe UI", 12, "bold"),
            text_color=COLORS["accent_purple"],
        )
        self.ttt_status.pack(pady=(0, 8))

        board_frame = ctk.CTkFrame(ttt_card.content, fg_color="transparent")
        board_frame.pack()

        self.ttt_board = [["" for _ in range(3)] for _ in range(3)]
        self.ttt_buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

        for r in range(3):
            for c in range(3):
                btn = ctk.CTkButton(
                    board_frame,
                    text="",
                    width=60,
                    height=60,
                    font=("Segoe UI Black", 20, "bold"),
                    fg_color=COLORS["bg_card"],
                    hover_color=COLORS["bg_card_hover"],
                    command=lambda row=r, col=c: self.make_ttt_move(row, col),
                )
                btn.grid(row=r, column=c, padx=4, pady=4)
                self.ttt_buttons[r][c] = btn

    def play_rps(self, move):
        choices = ["rock", "paper", "scissors"]
        comp = random.choice(choices)
        if move == comp:
            res = f"Tie! Both chose {move.capitalize()}."
        elif (move == "rock" and comp == "scissors") or (move == "paper" and comp == "rock") or (move == "scissors" and comp == "paper"):
            res = f"You Win! {move.capitalize()} beats {comp.capitalize()}! 🎉"
        else:
            res = f"You Lost! {comp.capitalize()} beats {move.capitalize()}."
        self.rps_status.configure(text=res)

    def check_guess(self):
        val = self.guess_entry.get().strip()
        if not val.isdigit():
            return
        guess = int(val)
        self.attempts += 1

        if guess < self.secret_num:
            self.guess_lbl.configure(text=f"Too low! (Attempt #{self.attempts})")
        elif guess > self.secret_num:
            self.guess_lbl.configure(text=f"Too high! (Attempt #{self.attempts})")
        else:
            self.guess_lbl.configure(text=f"🎉 Correct! The number was {self.secret_num}!")
            self.secret_num = random.randint(1, 100)
            self.attempts = 0

    def make_ttt_move(self, r, c):
        if self.ttt_board[r][c] != "":
            return
        self.ttt_board[r][c] = self.current_player
        self.ttt_buttons[r][c].configure(
            text=self.current_player,
            text_color=COLORS["accent_purple"] if self.current_player == "X" else COLORS["accent_cyan"]
        )

        # Check winner
        if self.check_ttt_winner(self.current_player):
            self.ttt_status.configure(text=f"🎉 Player {self.current_player} Wins!")
            self.after(1500, self.reset_ttt)
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.ttt_status.configure(text=f"Player {self.current_player}'s turn")

    def check_ttt_winner(self, p):
        b = self.ttt_board
        return any(all(b[r][c] == p for c in range(3)) for r in range(3)) or \
               any(all(b[r][c] == p for r in range(3)) for c in range(3)) or \
               all(b[i][i] == p for i in range(3)) or \
               all(b[i][2 - i] == p for i in range(3))

    def reset_ttt(self):
        self.ttt_board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.ttt_status.configure(text="Player X's turn")
        for r in range(3):
            for c in range(3):
                self.ttt_buttons[r][c].configure(text="")
