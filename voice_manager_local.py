import pyttsx3
import speech_recognition as sr

class VoiceManagerLocal:
    
    def __init__(self, wake-word = "hey chef", voice = "alloy"):
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 1.0)
        self.recongnizer = sr.Recognizer()
        self.wake_word = wake_word.lower()
        self.command_timeout = command_timeout
       
    def speak(self, text: str):
        
        try:
            self.engine.say(text) 
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error speaking: {e}")
            
    def listen(self, prompt = "Say Something", duration = 5):
        print(prompt)
        
        try:
            audio = self.recongnizer.listen(source, timeout=duration)
            text = self.recongnizer.recognize_google(audio)
            return text.lower().strip()
        except sr.UnknownValueError:
            print("STT could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"STT request error: {e}")
            return None
        except Exception as e:
            print(f"Error listening: {e}")
            return None
        
    def wait_for_wake_and_command(self):
        
        print(f"Waiting for {self.wake_word}...")
        
        while True:
            text = self.listen(prompt = "Say activation phrase...")
            
            #TODO: finish this logic to handle multiple wake words and commands
            