import os
import tempfile
import pygame
import sounddevice as sd
import scipy.io.wavfile as wav
from openai import OpenAI

class VoiceManagerGPT:

    """_summary_
    """
    # Initialize the voice manager with OpenAI API key, voice settings, wake word, and command timeout.
    def __init__(
        self, api_key=None, voice="alloy", wake_word="hey chef", command_timeout=10):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.voice  = voice
        self.wake_word = wake_word.lower()
        self.command_timeout = command_timeout
        pygame.mixer.init()

    # Speak the given text using the specified voice.
    def speak(self, text: str):
        try:
            with self.client.audio.speech.with_streaming_response.create(
                model = 'gpt-4o-mini-tts',
                voice = self.voice,
                input = text
            ) as response:
                tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                response.stream_to_file(tmp_file.name)
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    continue
        except Exception as e:
            print(f"Error in TTS: {e}")

    # Listen for a command and return it if detected.
    def listen(self, prompt = "Say Something", duration = 5):
        fs = 16000

        print(prompt)

        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        wav.write(tmp_file.name, fs, recording)

        try:
            transcript = self.client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe", file=open(tmp_file.name, "rb")
            )
            return transcript.text.lower().strip()
        except Exception as e:
            print("STT error:", e)
            return None
        
    # Wait for the wake word and then listen for a command.
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
                    self.speak("I didn’t hear a command, going back to standby.")
                    return "unknown"

    # Parse the command text and return the corresponding action.
    def parse_command(self, text: str):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a cooking assistant. Map user text to one of: "
                            "[next, repeat, clarify, grocery, switch_step, switch_all, unknown]."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
            )
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            print("Parse error:", e)
            return "unknown"
