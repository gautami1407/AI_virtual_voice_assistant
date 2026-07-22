# 🤖 BUJJI AI – Modern Desktop Assistant

<div align="center">

<img src="assets/bujji.gif" alt="BUJJI AI" width="180"/>

### Your Intelligent AI Desktop Companion

**BUJJI AI** is a modern cross-platform desktop assistant built with **Python**, **CustomTkinter**, and **Google Gemini AI**. It combines conversational AI, voice interaction, system automation, productivity tools, document intelligence, and developer utilities into a single elegant desktop application.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Modern_UI-blue?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-4285F4?style=for-the-badge&logo=google)
![Platform](https://img.shields.io/badge/Platform-Windows-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

*A modern AI desktop assistant inspired by ChatGPT, Microsoft Copilot, Siri and Google Assistant.*

</div>

---

# ✨ Features

## 🤖 AI Assistant

- Google Gemini AI integration
- Context-aware conversations
- Persistent chat history
- SQLite-powered memory
- Multiple AI personality modes
- Prompt templates
- Code generation
- Bug fixing assistance
- Explanation mode

---

## 🎤 Voice Assistant

- Voice command recognition
- Text command mode
- Wake word support
- Speech-to-Text
- Text-to-Speech
- Live voice waveform visualization
- Continuous listening mode

---

## 💬 Modern Chat Interface

- ChatGPT-inspired interface
- User & AI chat bubbles
- Typing animation
- Code block rendering
- Copy responses
- Conversation timestamps
- Sidebar navigation

---

## 📊 System Dashboard

Monitor your system in real time.

- CPU Usage
- RAM Usage
- Disk Usage
- Battery Status
- Running Processes
- Application Launcher

Launch

- VS Code
- Chrome
- Notepad
- Calculator
- File Explorer
- Command Prompt

---

## 🌤 Weather Dashboard

- Live weather lookup
- Temperature
- Humidity
- Wind Speed
- Global city search

---

## 📰 News Dashboard

Latest news categories

- Technology
- Artificial Intelligence
- India
- World News

Powered using Google News RSS.

---

## 📁 Document AI

- PDF Text Extraction
- AI Summarization
- Document Question Answering
- File Browser

---

## ⚡ Productivity Suite

- Pomodoro Timer
- Todo List
- Reminder Manager
- QR Code Generator
- Strong Password Generator

---

## 👨‍💻 Developer Hub

Built especially for developers.

- Python Prompt Templates
- SQL Generator
- HTML/CSS Generator
- Docker Commands
- Git Commands
- Linux Commands
- Debug Assistant

---

## 🎮 Entertainment

- AI Story Generator
- Jokes
- Mini Games

---

# 🎨 Modern User Interface

BUJJI AI features a modern desktop UI designed with **CustomTkinter**.

### Design Highlights

- Dark Theme
- Glassmorphism Inspired Layout
- Responsive Sidebar
- ChatGPT Style Chat Window
- Animated Voice Wave
- Purple & Cyan Accent Theme
- Smooth Navigation

---

# 🏗 Architecture

```
User
   │
   ▼
CustomTkinter UI
   │
   ▼
Application Controller
   │
   ├─────────────── AI Engine
   │                  │
   │                  ▼
   │            Google Gemini API
   │
   ├────────────── Voice Engine
   │                  │
   │          Speech Recognition
   │
   ├────────────── Database
   │                  │
   │               SQLite
   │
   ├────────────── System Automation
   │
   └────────────── Productivity Modules
```

---

# 📂 Project Structure

```
AI_virtual_voice_assistant/

│
├── main.py
├── requirements.txt
├── README.md
├── .env.example
│
├── bujji/
│
├── ui/
│   ├── sidebar.py
│   ├── landing_page.py
│   ├── chat_page.py
│   ├── voice_page.py
│   ├── weather_page.py
│   ├── news_page.py
│   ├── reminders_page.py
│   ├── productivity_page.py
│   ├── developer_page.py
│   ├── settings_page.py
│   └── system_monitor.py
│
├── ai/
├── voice/
├── automation/
├── productivity/
├── data/
│
├── assets/
│   └── bujji.gif
│
└── bujji.db
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/gautami1407/AI_virtual_voice_assistant.git

cd AI_virtual_voice_assistant
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file from `.env.example`.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY

WEATHER_API_KEY=YOUR_OPENWEATHER_API_KEY

HF_TOKEN=YOUR_HUGGINGFACE_TOKEN
```

---

## Run BUJJI

```bash
python main.py
```

or

```bash
python -m bujji
```

---

# 🔐 Security

BUJJI follows secure development practices.

- Environment Variables
- No Hardcoded API Keys
- Git Ignore Protection
- Portable Asset Loading
- Cross-platform File Management

---

# 📦 Technologies Used

### Languages

- Python

### Desktop UI

- CustomTkinter
- Tkinter

### Artificial Intelligence

- Google Gemini API

### Voice Processing

- SpeechRecognition
- pyttsx3

### Computer Vision

- OpenCV

### Automation

- PyAutoGUI
- psutil

### Database

- SQLite

### APIs

- Google Gemini
- OpenWeatherMap
- Google News RSS
- Wikipedia

### Python Libraries

- Pillow
- Requests
- BeautifulSoup
- PyJokes
- Pathlib

---

# 📌 Current Modules

- ✅ AI Chat
- ✅ Voice Assistant
- ✅ Wake Word
- ✅ Chat History
- ✅ Weather Dashboard
- ✅ News Dashboard
- ✅ System Monitor
- ✅ Productivity Tools
- ✅ Reminder Manager
- ✅ PDF AI
- ✅ QR Generator
- ✅ Password Generator
- ✅ Developer Assistant
- ✅ Mini Games
- ✅ Application Launcher

---

# 🚀 Future Roadmap

- Mobile Companion App
- Offline AI Models
- Plugin Marketplace
- Multi-language Support
- Face Recognition Login
- Smart Home Integration
- Voice Authentication
- Cloud Sync
- OCR Image Understanding
- Screen Understanding

---

# 🤝 Contributing

Contributions are welcome!

```bash
Fork the repository

↓

Create a new branch

↓

Implement your feature

↓

Commit changes

↓

Push your branch

↓

Open a Pull Request
```

---

# 📜 License

Licensed under the **MIT License**.

---

# 👩‍💻 Developer

## Nuchu Gouthami

**AI Developer | Python Developer | Cloud Computing Enthusiast | Open Source Contributor**

- 🌐 GitHub: https://github.com/gautami1407

---

<div align="center">

### ⭐ If you found this project helpful, consider giving it a Star!

**Made with ❤️ using Python & AI**

</div>
