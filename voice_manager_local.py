# import pyttsx3
# import speech_recognition as sr
# from command_utils import normalize_command, COMMAND_SET

# class VoiceManagerLocal:

#     def __init__(self, wake_word = "hey chef", voice = "alloy"):

#         self.engine = pyttsx3.init()
#         self.engine.setProperty('rate', 180)
#         self.engine.setProperty('volume', 1.0)
#         self.recongnizer = sr.Recognizer()
#         self.wake_word = wake_word.lower()
#         self.command_timeout = command_timeout

#     def speak(self, text: str):

#         try:
#             self.engine.say(text)
#             self.engine.runAndWait()
#         except Exception as e:
#             print(f"Error speaking: {e}")

#     def listen(self, prompt = "Say Something", duration = 5):
#         print(prompt)

#         try:
#             audio = self.recongnizer.listen(source, timeout=duration)
#             text = self.recongnizer.recognize_google(audio)
#             return text.lower().strip()
#         except sr.UnknownValueError:
#             print("STT could not understand audio")
#             return None
#         except sr.RequestError as e:
#             print(f"STT request error: {e}")
#             return None
#         except Exception as e:
#             print(f"Error listening: {e}")
#             return None

#     def wait_for_wake_and_command(self):

#         print(f"Waiting for {self.wake_word}...")

#         while True:
#             text = self.listen(prompt = "Say activation phrase...")

#             if text and self.wake_word in text:
#                 print(f"Wake word detected!")
#                 self.speak("Yes, how can I help?")

#                 command_text = self.listen(prompt = "Say your command...")

#                 if command_text:
#                     return self.parse_command(command_text)
#                 else:
#                     self.speak("I didn't catch that. Please try again.")
#                     return "unknown"

#     def parse_command(self, text: str):
#         if "next" in text:
#             return "next"
#         elif "repeat" in text:
#             return "repeat"
#         elif "clarify" in text or "tip" in text:
#             return "clarify"
#         elif "step" in text:
#             return "step"
#         elif "all" in text:
#             return "switch_all"
#         else:
#             return "unknown"
#             #TODO: finish this logic to handle multiple wake words and commands

# Version 2:
# import pyttsx3
# import speech_recognition as sr
# from command_utils import normalize_command, COMMAND_SET


# class VoiceManagerLocal:
#     """
#     Local voice assistant using pyttsx3 (TTS) and SpeechRecognition (Google/Sphinx).
#     Handles wake word, offline command mapping, and optional recipe title detection.
#     """

#     def __init__(self, wake_word="hey chef", command_timeout=10, voice=None):
#         # --- Text to Speech ---
#         self.engine = pyttsx3.init()
#         self.engine.setProperty("rate", 180)
#         self.engine.setProperty("volume", 1.0)

#         # Optional: match a specific voice name
#         if voice:
#             voices = self.engine.getProperty("voices")
#             for v in voices:
#                 if voice.lower() in v.name.lower():
#                     self.engine.setProperty("voice", v.id)
#                     break

#         # --- Speech Recognition ---
#         self.recognizer = sr.Recognizer()
#         self.wake_word = wake_word.lower()
#         self.command_timeout = command_timeout

#     # ---------- TTS ----------
#     def speak(self, text: str):
#         """Speak text aloud using pyttsx3."""
#         try:
#             self.engine.say(text)
#             self.engine.runAndWait()
#         except Exception as e:
#             print(f"TTS error: {e}")

#     # ---------- STT ----------
#     def listen(self, prompt="Say something", duration=5):
#         """Listen from microphone and return recognized text."""
#         print(prompt)
#         with sr.Microphone() as source:
#             try:
#                 self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
#                 audio = self.recognizer.listen(
#                     source, timeout=duration, phrase_time_limit=duration
#                 )
#                 text = self.recognizer.recognize_google(audio)
#                 return text.lower().strip()
#             except sr.WaitTimeoutError:
#                 print("Listening timed out.")
#                 return None
#             except sr.UnknownValueError:
#                 print("Speech not understood.")
#                 return None
#             except sr.RequestError as e:
#                 print(f"Speech recognition request error: {e}")
#                 return None
#             except Exception as e:
#                 print(f"Error listening: {e}")
#                 return None

#     # ---------- Wake + Command ----------
#     def wait_for_wake_and_command(self):
#         """
#         Wait for wake word, then capture next spoken command.
#         Returns either a system command from COMMAND_SET or raw text.
#         """
#         print(f"🎙 Waiting for wake word: '{self.wake_word}'")
#         while True:
#             heard = self.listen(prompt="Say activation phrase...", duration=4)
#             if heard and self.wake_word in heard:
#                 print("Wake word detected!")
#                 self.speak("Yes, how can I help?")

#                 command_text = self.listen(
#                     prompt="Listening for command...", duration=self.command_timeout
#                 )
#                 if not command_text:
#                     self.speak("I didn’t hear a command. Going back to standby.")
#                     return "unknown"

#                 parsed = normalize_command(command_text)
#                 # Return parsed if known, else raw text for recipe matching
#                 return parsed if parsed != "unknown" else command_text.lower()

# Version 3:
import pyttsx3
import speech_recognition as sr
from command_utils import normalize_command


class VoiceManagerLocal:
    """Local TTS/STT with wake word and shared command parsing."""

    def __init__(
        self, wake_word="hey chef", command_timeout=10, voice=None, mic_duration=5
    ):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)
        self.engine.setProperty("volume", 1.0)
        if voice:
            for v in self.engine.getProperty("voices"):
                if voice.lower() in v.name.lower():
                    self.engine.setProperty("voice", v.id)
                    break
        self.recognizer = sr.Recognizer()
        self.wake_word = wake_word.lower()
        self.command_timeout = command_timeout
        self.mic_duration = mic_duration

    def speak(self, text: str):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print("TTS error:", e)

    def calibrate(self, seconds: int = 2):
        """Ambient noise calibration using SpeechRecognition."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=seconds)
            self.speak("Calibration complete.")
        except Exception as e:
            print("Calibration error:", e)
            self.speak("Calibration skipped due to an error.")

    def listen(self, prompt="Say something", duration=None):
        dur = duration if duration is not None else self.mic_duration
        print(prompt)
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source, timeout=dur, phrase_time_limit=dur
                )
                text = self.recognizer.recognize_google(audio)
                text = text.lower().strip()
                print("🗣️ You said:", text)
                return text
            except Exception:
                return None

    def wait_for_wake_and_command(self):
        print(f"🎙 Waiting for wake word: '{self.wake_word}'")
        while True:
            heard = self.listen(prompt="Say activation phrase...", duration=4)
            if heard and self.wake_word in heard:
                self.speak("Yes, how can I help?")
                cmd_text = self.listen(
                    prompt="Listening for command...", duration=self.command_timeout
                )
                if not cmd_text:
                    self.speak("I didn’t hear a command. Going back to standby.")
                    return "unknown"
                parsed = normalize_command(cmd_text)
                return parsed if parsed != "unknown" else cmd_text.lower()
