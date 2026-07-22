"""
App Window — Main application window for BUJJI AI
===================================================
Hosts the top-level CTk window, sidebar navigation, and main content area.
Manages page switching and layout responsive resizing across all feature tabs.
"""

import customtkinter as ctk
from bujji.config import WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WIDTH, MIN_HEIGHT, APP_NAME
from bujji.ui.theme import COLORS
from bujji.ui.sidebar import Sidebar
from bujji.ui.landing_page import LandingPage
from bujji.ui.chat_page import ChatPage
from bujji.ui.voice_page import VoicePage
from bujji.ui.system_monitor import SystemMonitorPage
from bujji.ui.weather_page import WeatherPage
from bujji.ui.news_page import NewsPage
from bujji.ui.reminders_page import RemindersPage
from bujji.ui.camera_page import CameraPage
from bujji.ui.games_page import GamesPage
from bujji.ui.settings_page import SettingsPage
from bujji.ui.files_page import FilesPage
from bujji.ui.productivity_page import ProductivityPage
from bujji.ui.developer_page import DeveloperPage


class AppWindow(ctk.CTk):
    """
    Main application CTk Window.
    Contains:
    - Sidebar navigation (left)
    - Content container (right)
    - Page switching router for all features
    """

    def __init__(self, user_name="Gouthami", on_navigate_callback=None, app_controller=None, **kwargs):
        super().__init__(**kwargs)

        # Configure CTk appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window settings
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.configure(fg_color=COLORS["bg_primary"])

        self._user_name = user_name
        self._on_navigate_callback = on_navigate_callback
        self.app_controller = app_controller
        self.pages = {}
        self.current_page_key = "home"

        # Configure main grid (0: Sidebar, 1: Main Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ─── Sidebar ──────────────────────────────────────────────────────────
        self.sidebar = Sidebar(
            self,
            user_name=user_name,
            on_navigate=self.show_page,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # ─── Container Frame for Content Pages ───────────────────────────────
        self.container = ctk.CTkFrame(self, fg_color=COLORS["bg_primary"], corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize all pages
        self._init_pages()

        # Display default page
        self.show_page("home")

    def _init_pages(self):
        """Create page instances and place them into the container."""
        # 1. Home
        self.landing_page = LandingPage(self.container, user_name=self._user_name, on_action=self.show_page)
        self.landing_page.grid(row=0, column=0, sticky="nsew")
        self.pages["home"] = self.landing_page

        # 2. Voice Chat
        self.voice_page = VoicePage(self.container)
        self.voice_page.grid(row=0, column=0, sticky="nsew")
        self.pages["voice"] = self.voice_page

        # 3. AI Chat
        self.chat_page = ChatPage(self.container, on_new_chat=None)
        self.chat_page.grid(row=0, column=0, sticky="nsew")
        self.pages["chat"] = self.chat_page

        # 4. Productivity Tools
        self.tools_page = ProductivityPage(self.container, app_controller=self.app_controller)
        self.tools_page.grid(row=0, column=0, sticky="nsew")
        self.pages["tools"] = self.tools_page

        # 5. Developer Hub
        self.developer_page = DeveloperPage(self.container, app_controller=self.app_controller)
        self.developer_page.grid(row=0, column=0, sticky="nsew")
        self.pages["developer"] = self.developer_page

        # 4. Files
        self.files_page = FilesPage(self.container)
        self.files_page.grid(row=0, column=0, sticky="nsew")
        self.pages["files"] = self.files_page

        # 5. Weather
        self.weather_page = WeatherPage(self.container)
        self.weather_page.grid(row=0, column=0, sticky="nsew")
        self.pages["weather"] = self.weather_page

        # 6. News
        self.news_page = NewsPage(self.container)
        self.news_page.grid(row=0, column=0, sticky="nsew")
        self.pages["news"] = self.news_page

        # 7. Reminders
        self.reminders_page = RemindersPage(self.container)
        self.reminders_page.grid(row=0, column=0, sticky="nsew")
        self.pages["reminders"] = self.reminders_page

        # 8. Camera
        self.camera_page = CameraPage(self.container)
        self.camera_page.grid(row=0, column=0, sticky="nsew")
        self.pages["camera"] = self.camera_page

        # 9. Games
        self.games_page = GamesPage(self.container)
        self.games_page.grid(row=0, column=0, sticky="nsew")
        self.pages["games"] = self.games_page

        # 10. Settings
        self.settings_page = SettingsPage(self.container, app_controller=self.app_controller)
        self.settings_page.grid(row=0, column=0, sticky="nsew")
        self.pages["settings"] = self.settings_page

        # 11. System Monitor
        self.monitor_page = SystemMonitorPage(self.container)
        self.monitor_page.grid(row=0, column=0, sticky="nsew")
        self.pages["monitor"] = self.monitor_page

    def show_page(self, key):
        """Switch the visible content page."""
        if key not in self.pages:
            return

        page = self.pages[key]
        page.tkraise()
        self.current_page_key = key

        # Sync sidebar selection state without recursive loop
        self.sidebar.set_active(key)

        if self._on_navigate_callback:
            self._on_navigate_callback(key)
