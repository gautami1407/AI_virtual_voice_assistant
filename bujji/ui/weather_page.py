"""
Weather Page — Live Weather Dashboard & Forecast
================================================
Lookup weather conditions by city name with temperature, humidity, wind, and conditions.
"""

import threading
import requests
import customtkinter as ctk
from bujji.config import WEATHER_API_KEY
from bujji.ui.theme import COLORS, SPACING, RADIUS
from bujji.ui.components.glass_card import GlassCard


class WeatherPage(ctk.CTkFrame):
    """
    Weather Dashboard view page.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_primary"], **kwargs)

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
            text="🌤  Weather Dashboard",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Check current weather conditions and forecasts for any city worldwide",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            anchor="w",
        ).pack(fill="x", pady=(4, 0))

        # Search Bar Card
        search_card = GlassCard(self._scroll)
        search_card.pack(fill="x", pady=(0, SPACING["xl"]))

        search_row = ctk.CTkFrame(search_card.content, fg_color="transparent")
        search_row.pack(fill="x")
        search_row.columnconfigure(0, weight=1)

        self.city_entry = ctk.CTkEntry(
            search_row,
            placeholder_text="Enter city name (e.g. Hyderabad, London, New York)...",
            font=("Segoe UI", 13),
            fg_color=COLORS["bg_input"],
            height=40,
        )
        self.city_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.city_entry.bind("<Return>", lambda e: self.search_weather())

        btn = ctk.CTkButton(
            search_row,
            text="🔍 Fetch Weather",
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent_purple"],
            hover_color=COLORS["accent_purple_hover"],
            height=40,
            command=self.search_weather,
        )
        btn.grid(row=0, column=1)

        # Weather Display Card
        self.result_card = GlassCard(self._scroll, title="📍 City Weather Report")
        self.result_card.pack(fill="x", pady=(0, SPACING["xl"]))

        self.city_lbl = ctk.CTkLabel(
            self.result_card.content,
            text="Search for a city above...",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        self.city_lbl.pack(fill="x")

        self.temp_lbl = ctk.CTkLabel(
            self.result_card.content,
            text="-- °C",
            font=("Segoe UI Black", 48, "bold"),
            text_color=COLORS["accent_cyan"],
            anchor="w",
        )
        self.temp_lbl.pack(fill="x", pady=(8, 0))

        self.details_lbl = ctk.CTkLabel(
            self.result_card.content,
            text="",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            justify="left",
            anchor="w",
        )
        self.details_lbl.pack(fill="x", pady=(8, 0))

    def search_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            return

        self.city_lbl.configure(text=f"Fetching weather for {city}...")

        def _fetch():
            try:
                api_key = WEATHER_API_KEY
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}"
                resp = requests.get(url, timeout=5)
                data = resp.json()

                if resp.status_code == 200:
                    temp = round(data['main']['temp'])
                    cond = data['weather'][0]['description'].capitalize()
                    humidity = data['main']['humidity']
                    wind = data['wind']['speed']
                    country = data['sys'].get('country', '')

                    def _update_ui():
                        self.city_lbl.configure(text=f"📍 {data['name']}, {country}")
                        self.temp_lbl.configure(text=f"{temp}°C ({cond})")
                        self.details_lbl.configure(
                            text=f"💧 Humidity: {humidity}%  •  💨 Wind Speed: {wind} m/s"
                        )

                    def _safe_after(fn):
                        try:
                            if self.winfo_exists():
                                self.after(0, fn)
                        except Exception:
                            pass

                    _safe_after(_update_ui)
                else:
                    try:
                        if self.winfo_exists():
                            self.after(0, lambda: self.city_lbl.configure(text=f"❌ City '{city}' not found."))
                    except Exception:
                        pass
            except Exception as e:
                try:
                    if self.winfo_exists():
                        self.after(0, lambda: self.city_lbl.configure(text=f"⚠️ Error fetching weather: {e}"))
                except Exception:
                    pass

        threading.Thread(target=_fetch, daemon=True).start()
