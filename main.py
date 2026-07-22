"""
Smart Talk - AI Virtual Voice Assistant
======================================
Main application entry point.

CHANGES MADE:
- Removed hardcoded absolute file path (C:\\Users\\N.SIRISHA\\OneDrive\\...)
- Removed hardcoded API tokens (secrets moved to environment variables)
- Added portable asset loading using assets module
- All asset paths are now relative to project root
- Missing assets are handled gracefully with warnings and placeholders
- Compatible with Windows, Linux, and macOS
"""

import itertools
import sys
import threading
import tkinter as tk
from tkinter import Scrollbar, END
from PIL import Image, ImageTk
import features as ft
import functions as func
from gui import root,text_area,update_text_area
import assets
import os

# Load secrets from environment variables (secure approach)
# Copy .env.example to .env and fill in your values
weather_api_key = os.environ.get("WEATHER_API_KEY", "")
headers = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN', '')}"}

intro = "Hello, I'm smart talk,a voice assistant.plz command me What to do?"
appreciations = ["well done", "keep it up", "great job"]

# Global reference to keep animated GIF app instance
_animated_gif_app = None


def processCommand(query, story=None):
    if "open google" in query:
        func.speak("Opening Google...")
        ft.open_google()
    elif "open youtube" in query:
        func.speak("Opening YouTube...")
        ft.open_youtube()

    elif "weather" in query:
        func.speak("tell me the city name you want to know the weather")
        city = func.listen()
        if city:
            func.speak(f"you asked weather for {city} city")
            weather_data = ft.get_weather(city, weather_api_key)
            if weather_data:
                if weather_data.get('cod') == 404:
                    func.speak("No city found.")
                    ft.messagebox.showerror("Error", "No city found.")
                else:
                    weather = weather_data['weather'][0]['description']
                    temp = round(weather_data['main']['temp'])
                    humidity = weather_data['main']['humidity']
                    wind_speed = weather_data['wind']['speed']
                    details_speak = (
                        f"The weather in {city} is currently {weather}. "
                        f"The temperature is {temp} degrees Fahrenheit. "
                        f"The humidity is {humidity} percent, "
                        f"and the wind speed is {wind_speed} miles per hour."
                    )
                    threading.Thread(target=func.speak, args=(details_speak,)).start()
                    ft.show_weather_details(city, weather, temp, humidity, wind_speed)
            else:
                func.speak("Let's try again later.")

    elif "search youtube for" in query:
        func.speak("Searching YouTube...")
        ft.youtube_search(query)
    elif "search google for" in query:
        func.speak("Searching Google...")
        ft.google_search(query)
    elif query in appreciations:
        response = ft.respond(query)
        if response:
            func.speak(response)
    elif "open file explorer" in query:
        func.speak("Opening File Explorer.")
        ft.open_file_explorer()
    elif "open notepad" in query:
        func.speak("Opening Notepad...")
        ft.notepad()
    elif "locate" in query:
        func.speak("Opening location...")
        ft.location(query)
    elif "joke" in query:
        joke = ft.jokes()
        func.speak(joke)
    elif "time" in query:
        current_time = ft.time()
        func.speak(f"The current time is {current_time}.")
    elif "open calendar" in query:
        func.speak("Opening Calendar.")
        ft.calendar()
    elif "open camera" in query:
        func.speak("Opening Camera...")
        ft.open_camera()
    elif "system status" in query:
        status = ft.sys_status()
        func.speak(status)
    elif "search wikipedia for" in query:
        result = ft.wiki(query)
        func.speak(result)
    elif "news headlines" in query:
        headlines = ft.fetch_headlines()
        func.speak(headlines)
        func.speak("If you want to know more about the news, give the 'show news' command.")
    elif "calculate" in query:
        result = ft.calculation(query)
        func.speak(f"The result is {result}.")
    elif "screenshot" in query:
        func.speak("Taking screenshot...")
        ft.screenshot()
    elif "news" in query:
        func.speak("Opening News...")
        ft.news()
    elif "add reminder" in query:
        ft.add_reminder(query)
        func.speak("Reminder added.")
    elif "show reminder" in query:
        func.speak("Showing reminders...")
        reminders = ft.show_reminder()
        if reminders:
            func.speak(reminders)
    elif "are you single" in query:
        ft.fun_response()
    elif "let's play" in query:
        func.speak("Opening Game Hub.")
        ft.play_game_hub()
    elif "exit" in query:
        func.speak("Goodbye, sir. Please wake me up when needed.")
        terminate_Bujji(root)
    else:
      ft.ai(query)


def initialize_animated_gif(root):
    """
    Initialize the animated GIF with portable, cross-platform path handling.
    
    Uses the assets module to find the GIF file relative to the project root.
    Handles missing files gracefully without crashing.
    
    Args:
        root: The tkinter root window
    
    Returns:
        True if GIF loaded successfully, False otherwise
    """
    global _animated_gif_app
    
    # Use the asset helper to get a portable path
    gif_path = assets.get_gif_path("bujji.gif")
    
    # Check if the GIF exists before attempting to load
    if not assets.asset_exists("bujji.gif", use_assets_subfolder=False):
        # Also check in assets subfolder
        if assets.asset_exists("bujji.gif", use_assets_subfolder=True):
            gif_path = assets.get_asset_path("bujji.gif", use_assets_subfolder=True)
        else:
            print(f"[WARNING] bujji.gif not found in {assets.PROJECT_ROOT}")
            print(f"         A placeholder will be shown instead.")
            return False
    
    try:
        _animated_gif_app = AnimatedGifApp(root, str(gif_path))
        return True
    except FileNotFoundError:
        print(f"[WARNING] Could not load bujji.gif from: {gif_path}")
        return False
    except Exception as e:
        print(f"[WARNING] Error loading GIF: {e}")
        return False


class AnimatedGifApp:
    """
    Animated GIF display class.
    Uses portable paths - the GIF path is provided by the caller.
    """
    def __init__(self, root, gif_path):
        self.root = root
        self.gif_path = gif_path
        self.gif_image = Image.open(self.gif_path)
        self.resize_width = 300
        self.resize_height = 200
        self.frames = [ImageTk.PhotoImage(frame.copy().resize((self.resize_width, self.resize_height)))
                       for frame in self._get_frames()]
        self.label = tk.Label(self.root)
        self.label.pack(pady=10)
        self.current_frame = itertools.cycle(self.frames)
        self._animate()

    def _get_frames(self):
        frames = []
        try:
            while True:
                frames.append(self.gif_image.copy())
                self.gif_image.seek(self.gif_image.tell() + 1)
        except EOFError:
            pass
        return frames

    def _animate(self):
        frame = next(self.current_frame)
        self.label.config(image=frame)
        self.root.after(100, self._animate)

def create_gui():
    global text_area, entry_field

    root.title("SMART TALK- Your AI Assistant")
    root.geometry("400x700")
    root.configure(bg="#0D1117")

    custom_font = ("Orbitron", 12)

    # Initialize Animated GIF (with portable path handling)
    # The GIF will be loaded from project root if available, with graceful fallback
    if not initialize_animated_gif(root):
        # If GIF fails to load, show a placeholder label instead
        placeholder_label = tk.Label(root, text="[Assistant Animation]", 
                                    font=("Orbitron", 16), bg="#0D1117", fg="#58A6FF")
        placeholder_label.pack(pady=10)

    # Assistant Label
    frame = tk.Frame(root, bg="#0D1117")
    frame.pack(pady=10)

    assistant_label = tk.Label(frame, text="SMART TALK - Assistant", font=("Orbitron", 18, "bold"),
                               bg="#0D1117", fg="#58A6FF")
    assistant_label.pack()

    # Button Hover Effects
    def on_enter(e):
        e.widget['background'] = '#58A6FF'

    def on_leave(e):
        e.widget['background'] = '#21262D'

    # Start Button
    start_button = tk.Button(root, text="Start", command=run_Bujji_thread, bg="#21262D",
                             fg="#FFFFFF", font=custom_font, relief="groove", width=20)
    start_button.pack(pady=10)
    start_button.bind("<Enter>", on_enter)
    start_button.bind("<Leave>", on_leave)

    # Exit Button
    exit_button = tk.Button(root, text="Exit", command=lambda: terminate_Bujji(root),
                            bg="#21262D", fg="#FFFFFF", font=custom_font, relief="groove", width=20)
    exit_button.pack(pady=5)
    exit_button.bind("<Enter>", on_enter)
    exit_button.bind("<Leave>", on_leave)

    # Chat Mode Button
    chat_mode_button = tk.Button(root, text="Switch to Chat Mode", command=switch_to_chat_mode,
                                 bg="#21262D", fg="#FFFFFF", font=custom_font, relief="groove", width=20)
    chat_mode_button.pack(pady=10)
    chat_mode_button.bind("<Enter>", on_enter)
    chat_mode_button.bind("<Leave>", on_leave)

    # Show Commands Button
    btn_show_commands = tk.Button(root, text="Show Commands",
                                  command=lambda: update_text_area(ft.showCommands()),
                                  bg="#21262D", fg="#FFFFFF", font=custom_font, relief="groove", width=20)
    btn_show_commands.pack(pady=10)
    btn_show_commands.bind("<Enter>", on_enter)
    btn_show_commands.bind("<Leave>", on_leave)

    # Text Area with Scrollbar
    scrollbar = Scrollbar(root, troughcolor="#21262D", bg="#58A6FF")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_area.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_area.yview)
    text_area.pack(pady=10)

    # Entry Field
    entry_field = tk.Entry(root, width=50, bg="cyan", fg="#C9D1D9",
                           font=("Arial", 10), relief="flat")
    entry_field.pack(pady=10)
    entry_field.bind("<Return>", process_chat_command)

    root.mainloop()

def run_Bujji_thread():
    Bujji_thread = threading.Thread(target=startBujji)
    Bujji_thread.daemon = True
    Bujji_thread.start()

stop_thread = threading.Event()

def terminate_Bujji(root):
    stop_thread.set()
    root.destroy()
    sys.exit()

def process_chat_command(event):
    command = entry_field.get()
    entry_field.delete(0, END)
    update_text_area(f"User: {command}")
    processCommand(command)

def switch_to_chat_mode():
    global entry_field, text_area
    entry_field.pack(pady=10)
    text_area.configure(state='normal')
    text_area.delete(1.0, END)
    text_area.pack()

def startBujji():
    func.speak(intro)
    while not stop_thread.is_set():
        command = func.takeCommand()
        if command:
            processCommand(command)


if __name__ == "__main__":
    create_gui()