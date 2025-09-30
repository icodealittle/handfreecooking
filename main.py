import tkinter as tk
import threading
from recipe_manager import RecipeManager
from voice_manager_gpt import VoiceManagerGPT
from cooking_session import CookingSession
from ui_manager import UIManager
from utils import log_event, load_config
from voice_manager_local import VoiceManagerLocal
# Handle voice commands in a separate thread
def handle_voice_command(session, voice_manager):
    while True:
        command = voice_manager.wait_for_wake_and_command()
        print(f"Received voice command: {command}")
        
        if command:
            log_event(f"Voice command received: {command}")
            if "start" in command:
                session.start(mode="step")
            elif "next" in command:
                session.next_step()
            elif "repeat" in command:
                session.repeat_step()
            elif "clarify" in command:
                session.clarify_step()
            elif "all" in command:
                session.start(mode="all")
            else:
                voice_manager.speak("Sorry, I didn't understand that command.")
                
# Main application setup
def main():
    config = load_config()
    
    root = tk.Tk()
    root.withdraw()
    
    recipe_manager = RecipeManager("recipes.json")
    voice_manager = VoiceManagerGPT(
        wake_word=config.get("wake_word", "hey chef"),
        voice=config.get("voice", "alloy"),
        command_timeout=config("command_timeout", 10)
    )
    
    voive_manager = VoiceManagerLocal(wake_word= "hey chef", command_timeout = 10)
    
    
    session = CookingSession(recipe_manager, voice_manager)
    ui = UIManager(root, recipe_manager, session)
    
    threading.Thread(target=handle_voice_command, args=(session, voice_manager), daemon=True).start()
    
    root.deiconify()
    root.mainloop()
    
if __name__ == "__main__":
    main()
