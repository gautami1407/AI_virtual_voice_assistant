import tkinter as tk
from tkinter import messagebox, ttk
import random
import functions as func


# Virtual Assistant GUI Class
class GameHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Assistant Game Hub")
        self.root.geometry("500x500")
        self.root.configure(bg="#f0f0f0")

        # Game Hub Title
        self.label = tk.Label(root, text="Welcome to the Game Hub!", font=('Helvetica', 20, 'bold'), bg="#f0f0f0",
                              fg="#4d4dff")
        self.label.pack(pady=20)

        # Game Buttons Frame
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(pady=10)

        # Game Buttons
        games = [
            ("Guess the Number", self.guess_the_number),
            ("Rock Paper Scissors", self.rock_paper_scissors),
            ("Tic-Tac-Toe", self.tic_tac_toe),
            ("Snake Game", self.snake_game),
            ("Escape Room", self.escape_room)
        ]

        for game in games:
            game_button = tk.Button(self.button_frame, text=game[0], command=game[1], width=25, font=('Helvetica', 14),
                                    bg="#4d4dff", fg="white", relief="raised")
            game_button.pack(pady=5)

    def guess_the_number(self):
        GuessTheNumberGame(tk.Toplevel(self.root))

    def rock_paper_scissors(self):
        RockPaperScissorsGame(tk.Toplevel(self.root))

    def tic_tac_toe(self):
        TicTacToe(tk.Toplevel(self.root))

    def snake_game(self):
        SnakeGame(tk.Toplevel(self.root))

    def escape_room(self):
        EscapeRoomGame(tk.Toplevel(self.root))


# Guess the Number Game Class
class GuessTheNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Number Game")
        self.create_main_menu()

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear any existing widgets
        ttk.Label(self.root, text="Welcome to Guess the Number Game", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=10)

    def start_game(self):
        self.attempts = 0
        self.number = random.randint(1, 100)
        self.create_game_window()

    def create_game_window(self):
        self.guess_window = tk.Toplevel(self.root)
        self.guess_window.title("Guess the Number")

        ttk.Label(self.guess_window, text="Guess a number between 1 and 100:", font=("Arial", 12)).pack(pady=10)

        self.guess_entry = ttk.Entry(self.guess_window)
        self.guess_entry.pack(pady=5)
        self.guess_entry.focus_set()  # Focus on the entry box for easier input

        ttk.Button(self.guess_window, text="Submit", command=self.check_guess).pack(pady=10)
        self.result_label = ttk.Label(self.guess_window, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess < self.number:
                self.result_label.config(text="Too low!", foreground="blue")
            elif guess > self.number:
                self.result_label.config(text="Too high!", foreground="red")
            else:
                messagebox.showinfo("Correct!", f"Correct! The number was {self.number}.\nAttempts: {self.attempts}")
                self.guess_window.destroy()
                self.play_again()

            self.guess_entry.delete(0, tk.END)  # Clear entry for the next guess
            self.guess_entry.focus_set()  # Focus back on entry for the next attempt

        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number.")
            self.guess_entry.delete(0, tk.END)  # Clear the entry box for re-entry

    def play_again(self):
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            self.start_game()
        else:
            self.create_main_menu()


# Rock Paper Scissors Game Class
class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.player_score = 0
        self.computer_score = 0
        self.create_main_menu()

        # Configure styles
        style = ttk.Style()
        style.configure("TButton", padding=10, font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12))

    def create_main_menu(self):
        # Main menu layout
        ttk.Label(self.root, text="Welcome to Rock Paper Scissors", font=("Arial", 24)).pack(pady=40)
        ttk.Button(self.root, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.create_game_window()

    def create_game_window(self):
        # Game window layout
        self.rps_window = tk.Toplevel(self.root)
        self.rps_window.title("Rock Paper Scissors")
        self.rps_window.geometry("400x300")
        self.rps_window.resizable(False, False)

        ttk.Label(self.rps_window, text="Choose your move:", font=("Arial", 16)).pack(pady=20)

        button_frame = ttk.Frame(self.rps_window)
        button_frame.pack(pady=10)

        for choice in ["Rock", "Paper", "Scissors"]:
            ttk.Button(button_frame, text=choice, command=lambda c=choice.lower(): self.play_rps(c)).pack(side=tk.LEFT,
                                                                                                          padx=10)

        self.score_label = ttk.Label(self.rps_window,
                                     text=f"Score - You: {self.player_score}, Computer: {self.computer_score}",
                                     font=("Arial", 14))
        self.score_label.pack(pady=20)

    def play_rps(self, player_choice):
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)

        if player_choice == computer_choice:
            result = "It's a tie!"
        elif (player_choice == "rock" and computer_choice == "scissors") or \
                (player_choice == "paper" and computer_choice == "rock") or \
                (player_choice == "scissors" and computer_choice == "paper"):
            result = "You win!"
            self.player_score += 1
        else:
            result = "You lose!"
            self.computer_score += 1

        messagebox.showinfo("Result",
                            f"You chose {player_choice.capitalize()}, computer chose {computer_choice.capitalize()}.\n{result}")
        self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Score - You: {self.player_score}, Computer: {self.computer_score}")
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            self.player_score = 0
            self.computer_score = 0
            self.update_score()
        else:
            self.rps_window.destroy()


# Tic Tac Toe Class
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x450")
        self.create_welcome_message()
        self.reset_game()
        self.create_board()

    def create_welcome_message(self):
        welcome_label = tk.Label(self.root, text="Welcome to Tic Tac Toe!", font=("Arial", 16))
        welcome_label.pack(pady=10)

    def create_board(self):
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(self.root, text="", font=("Arial", 40), width=5, height=2,
                                                   command=lambda r=row, c=col: self.make_move(r, c))
                self.buttons[row][col].grid(row=row, column=col, padx=10, pady=10)

        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Arial", 16), command=self.reset_game)
        self.reset_button.grid(row=3, column=0, columnspan=3, pady=20)

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state=tk.NORMAL)
        messagebox.showinfo("Game Reset", "The game has been reset. Player X goes first!")

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif all(cell != "" for row in self.board for cell in row):
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        return any(all(self.board[row][col] == player for col in range(3)) for row in range(3)) or \
               any(all(self.board[row][col] == player for row in range(3)) for col in range(3)) or \
               all(self.board[i][i] == player for i in range(3)) or \
               all(self.board[i][2 - i] == player for i in range(3))


# Snake Game Class
class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.create_welcome_message()
        # Placeholder for actual snake game logic
        self.start_game()

    def create_welcome_message(self):
        welcome_label = tk.Label(self.root, text="Welcome to Snake Game!", font=("Arial", 16))
        welcome_label.pack(pady=10)

    def start_game(self):
        messagebox.showinfo("Snake Game", "This is where the snake game will run!")
        self.root.destroy()  # Close the window after the placeholder message


# Escape Room Game Class
class EscapeRoomGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Escape Room Game")
        self.create_welcome_message()
        # Placeholder for actual escape room game logic
        self.start_game()

    def create_welcome_message(self):
        welcome_label = tk.Label(self.root, text="Welcome to Escape Room!", font=("Arial", 16))
        welcome_label.pack(pady=10)

    def start_game(self):
        messagebox.showinfo("Escape Room", "This is where the escape room game will run!")
        self.root.destroy()  # Close the window after the placeholder message


def start_game_hub():
    func.speak("Starting Game Hub...")  # Debugging output
    root = tk.Tk()
    app = GameHubApp(root)  # Make sure this is defined correctly
    root.mainloop()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = GameHubApp(root)
    root.mainloop()
