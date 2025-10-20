# import os
# import tempfile
# import pygame
# import sounddevice as sd
# import scipy.io.wavfile as wav
# from openai import OpenAI

# class VoiceManagerGPT:

#     """_summary_
#     """
#     # Initialize the voice manager with OpenAI API key, voice settings, wake word, and command timeout.
#     def __init__(
#         self, api_key=None, voice="alloy", wake_word="hey chef", command_timeout=10):
#         self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
#         self.voice  = voice
#         self.wake_word = wake_word.lower()
#         self.command_timeout = command_timeout
#         pygame.mixer.init()

#     # Speak the given text using the specified voice.
#     def speak(self, text: str):
#         try:
#             with self.client.audio.speech.with_streaming_response.create(
#                 model = 'gpt-4o-mini-tts',
#                 voice = self.voice,
#                 input = text
#             ) as response:
#                 tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
#                 response.stream_to_file(tmp_file.name)
#                 pygame.mixer.music.load(tmp_file.name)
#                 pygame.mixer.music.play()
#                 while pygame.mixer.music.get_busy():
#                     continue
#         except Exception as e:
#             print(f"Error in TTS: {e}")

#     # Listen for a command and return it if detected.
#     def listen(self, prompt = "Say Something", duration = 5):
#         fs = 16000

#         print(prompt)

#         recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
#         sd.wait()

#         tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
#         wav.write(tmp_file.name, fs, recording)

#         try:
#             transcript = self.client.audio.transcriptions.create(
#                 model="gpt-4o-mini-transcribe", file=open(tmp_file.name, "rb")
#             )
#             return transcript.text.lower().strip()
#         except Exception as e:
#             print("STT error:", e)
#             return None

#     # Wait for the wake word and then listen for a command.
#     def wait_for_wake_word(self):
#         print(f"Waiting for wake word: '{self.wake_word}'")
#         while True:
#             text = self.listen(prompt="Say activation phrase...")
#             if text and self.wake_word in text:
#                 print("Wake word detected!")
#                 self.speak("Yes, how can I help?")

#                 command_text = self.listen(
#                     prompt="Listening for command...", duration=self.command_timeout
#                 )
#                 if command_text:
#                     return self.parse_command(command_text)
#                 else:
#                     self.speak("I didn’t hear a command, going back to standby.")
#                     return "unknown"

#     # Parse the command text and return the corresponding action.
#     def parse_command(self, text: str):
#         try:
#             response = self.client.chat.completions.create(
#                 model="gpt-4.1-mini",
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": (
#                             "You are a cooking assistant. Map user text to one of: "
#                             "[next, repeat, clarify, grocery, switch_step, switch_all, unknown]."
#                         ),
#                     },
#                     {"role": "user", "content": text},
#                 ],
#             )
#             return response.choices[0].message.content.strip().lower()
#         except Exception as e:
#             print("Parse error:", e)
#             return "unknown"

# Version 2:

# import os
# import tempfile
# import pygame
# import sounddevice as sd
# import scipy.io.wavfile as wav
# from openai import OpenAI
# from command_utils import normalize_command, COMMAND_SET


# class VoiceManagerGPT:
#     """
#     Voice Manager using OpenAI GPT for speech-to-text (STT) and text-to-speech (TTS).
#     Unified with command_utils for consistent command parsing across local and GPT modes.
#     """

#     def __init__(
#         self, api_key=None, voice="alloy", wake_word="hey chef", command_timeout=10
#     ):
#         self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
#         self.voice = voice
#         self.wake_word = wake_word.lower()
#         self.command_timeout = command_timeout

#         # Initialize pygame for playback
#         pygame.mixer.init()

#     # ---------- TEXT TO SPEECH ----------
#     def speak(self, text: str):
#         """Speak text aloud using GPT TTS."""
#         try:
#             with self.client.audio.speech.with_streaming_response.create(
#                 model="gpt-4o-mini-tts", voice=self.voice, input=text
#             ) as response:
#                 tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
#                 response.stream_to_file(tmp_file.name)
#                 pygame.mixer.music.load(tmp_file.name)
#                 pygame.mixer.music.play()
#                 while pygame.mixer.music.get_busy():
#                     pygame.time.wait(100)  # prevent CPU spike
#         except Exception as e:
#             print(f"TTS Error: {e}")

#     # ---------- SPEECH TO TEXT ----------
#     def listen(self, prompt="Say something", duration=5):
#         """Record and transcribe audio using GPT transcription model."""
#         fs = 16000
#         print(prompt)
#         try:
#             recording = sd.rec(
#                 int(duration * fs), samplerate=fs, channels=1, dtype="int16"
#             )
#             sd.wait()

#             tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
#             wav.write(tmp_file.name, fs, recording)

#             transcript = self.client.audio.transcriptions.create(
#                 model="gpt-4o-mini-transcribe", file=open(tmp_file.name, "rb")
#             )
#             text = transcript.text.lower().strip()
#             print("🗣️ You said:", text)
#             return text
#         except Exception as e:
#             print(f"STT Error: {e}")
#             return None

#     # ---------- WAKE WORD + COMMAND ----------
#     def wait_for_wake_and_command(self):
#         """
#         Wait for wake word, then listen for the next spoken command.
#         Returns either a known command from COMMAND_SET or raw text (for recipes).
#         """
#         print(f"🎤 Waiting for wake word: '{self.wake_word}'")

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
#                 # Return normalized command if valid, otherwise the raw text (recipe title)
#                 return parsed if parsed != "unknown" else command_text.lower()

# Version 3:
import os
import tempfile
import pygame
import sounddevice as sd
import scipy.io.wavfile as wav
from openai import OpenAI


class VoiceManagerGPT:
    """Voice Manager that handles speech recognition (STT) and text-to-speech (TTS)
    using OpenAI's GPT-powered audio models.
    """

    def __init__(
        self,
        api_key=None,
        voice="alloy",
        wake_word="hey chef",
        command_timeout=10,
        config=None,
    ):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.voice = voice
        self.wake_word = wake_word.lower()
        self.command_timeout = command_timeout
        self.stt_model = "whisper-1"
        self.stt_language = "en"

        if config:
            self.stt_language = config.get("stt_language", "en")

        # ✅ Auto-detect first available input device
        try:
            devices = sd.query_devices()
            input_devices = [
                i for i, d in enumerate(devices) if d["max_input_channels"] > 0
            ]
            if input_devices:
                sd.default.device = input_devices[0]
                print(f"🎤 Using mic: {devices[input_devices[0]]['name']}")
            else:
                print("⚠️ No input device found. Falling back to text mode.")
        except Exception as e:
            print("⚠️ Could not query audio devices:", e)

        pygame.mixer.init()

    # ✅ Text-to-speech
    def speak(self, text: str):
        try:
            with self.client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts", voice=self.voice, input=text
            ) as response:
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                response.stream_to_file(tmp_file.name)
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    continue
        except Exception as e:
            print(f"Error in TTS: {e}")

    # ✅ Speech-to-text
    def listen(self, prompt="Say something...", duration=5):
        fs = 16000
        print(prompt)

        try:
            recording = sd.rec(
                int(duration * fs), samplerate=fs, channels=1, dtype="int16"
            )
            sd.wait()

            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            wav.write(tmp_file.name, fs, recording)

            kwargs = {"model": self.stt_model, "file": open(tmp_file.name, "rb")}
            if self.stt_language:
                kwargs["language"] = self.stt_language  # must be ISO-639-1, e.g., "en"

            transcript = self.client.audio.transcriptions.create(**kwargs)
            return transcript.text.lower().strip()
        except Exception as e:
            print("STT error:", e)
            return None

    # ✅ Wait for wake word, then command
    def wait_for_wake_word(self):
        print(f"Waiting for wake word: '{self.wake_word}'")
        while True:
            text = self.listen(prompt="Say activation phrase...")
            if text and self.wake_word in text:
                print("Wake word detected!")
                self.speak("Yes, how can I help?")

                command_text = self.listen(
                    prompt="Listening for command...", duration=self.command_timeout
                )
                if command_text:
                    return self.parse_command(command_text)
                else:
                    self.speak("I didn’t hear a command. Going back to standby.")
                    return "unknown"

    # ✅ Command parser via GPT
    def parse_command(self, text: str):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a cooking assistant. "
                            "Map the user's spoken text to one of: "
                            "[next, repeat, clarify, grocery, start, stop, switch_step, switch_all, unknown]."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
            )
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            print("Parse error:", e)
            return "unknown"
