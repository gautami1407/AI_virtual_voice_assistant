import speech_recognition as sr
import pyttsx3
from gui import update_text_area

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

calls = ["bujji", "hello bujji", "are you there", "wake up bujji", "time for work"]
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.5
        recognizer.dynamic_energy_ratio = 1.5
        recognizer.operation_timeout = None
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_adjustment_damping = 0.15
        recognizer.phrase_threshold = 0.3
        recognizer.non_speaking_duration = 0.5
        update_text_area("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio_data = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio_data)
            update_text_area(f"Speech recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            update_text_area("Could not understand the audio.")
        except sr.RequestError as e:
            update_text_area(f"Error: {e}")
        except sr.WaitTimeoutError:
            update_text_area("Listening timed out while waiting for phrase to start.")
    return None

def speak(text):
    update_text_area(f"smart talk says: {text}")
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    return listen()

def takeWakeupCommand():
    wake = listen()
    if wake in calls:
        return True
    return False

