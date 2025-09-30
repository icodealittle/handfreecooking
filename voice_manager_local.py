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
            
            if text and self.wake_word in text:
                print(f"Wake word detected!")
                self.speak("Yes, how can I help?")
                
                command_text = self.listen(prompt = "Say your command...")
                
                if command_text:
                    return self.parse_command(command_text)
                else:
                    self.speak("I didn't catch that. Please try again.")
                    return "unknown"
                
    def parse_command(self, text: str):
        if "next" in text:
            return "next"
        elif "repeat" in text:
            return "repeat"
        elif "clarify" in text or "tip" in text:
            return "clarify"
        elif "step" in text:
            return "step"
        elif "all" in text:
            return "switch_all"
        else:
            return "unknown"
            #TODO: finish this logic to handle multiple wake words and commands
            