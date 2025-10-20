# import tkinter as tk
# import threading
# from recipe_manager import RecipeManager
# from voice_manager_gpt import VoiceManagerGPT
# from cooking_session import CookingSession
# from ui_manager import UIManager
# from utils import log_event, load_config
# from voice_manager_local import VoiceManagerLocal
# # Handle voice commands in a separate thread
# def handle_voice_command(session, voice_manager):
#     while True:
#         command = voice_manager.wait_for_wake_and_command()
#         print(f"Received voice command: {command}")

#         if command:
#             log_event(f"Voice command received: {command}")
#             if "start" in command:
#                 session.start(mode="step")
#             elif "next" in command:
#                 session.next_step()
#             elif "repeat" in command:
#                 session.repeat_step()
#             elif "clarify" in command:
#                 session.clarify_step()
#             elif "all" in command:
#                 session.start(mode="all")
#             else:
#                 voice_manager.speak("Sorry, I didn't understand that command.")

# # Main application setup
# def main():
#     config = load_config()

#     root = tk.Tk()
#     root.withdraw()

#     recipe_manager = RecipeManager("recipes.json")
#     voice_manager = VoiceManagerGPT(
#         wake_word=config.get("wake_word", "hey chef"),
#         voice=config.get("voice", "alloy"),
#         command_timeout=config("command_timeout", 10)
#     )

#     voive_manager = VoiceManagerLocal(wake_word= "hey chef", command_timeout = 10)


#     session = CookingSession(recipe_manager, voice_manager)
#     ui = UIManager(root, recipe_manager, session)

#     threading.Thread(target=handle_voice_command, args=(session, voice_manager), daemon=True).start()

#     root.deiconify()
#     root.mainloop()

# if __name__ == "__main__":
#     main()

# Version 2:
# import tkinter as tk
# import threading
# from recipe_manager import RecipeManager
# from voice_manager_gpt import VoiceManagerGPT
# from cooking_session import CookingSession
# from ui_manager import UIManager
# from utils import load_config

# # Import both voice managers
# from voice_manager_gpt import VoiceManagerGPT
# from voice_manager_local import VoiceManagerLocal


# def handle_voice_commands(session, voice_manager):
#     """
#     Background loop for voice wake + commands.
#     Waits for wake word, then executes cooking commands.
#     """
#     while True:
#         command = voice_manager.wait_for_wake_and_command()
#         print("Command received:", command)

#         if command == "next":
#             session.next_step()
#         elif command == "repeat":
#             session.repeat_step()
#         elif command == "clarify":
#             session.clarify_step()
#         elif command == "switch_step":
#             session.start("step")
#         elif command == "switch_all":
#             session.start("all")
#         else:
#             voice_manager.speak("Sorry, I didn't understand.")


# def main():
#     # Load settings
#     config = load_config()

#     root = tk.Tk()
#     root.withdraw()

#     # Setup Recipe Manager
#     recipe_manager = RecipeManager(
#         "recipes.json",
#         api_key=config.get("openai_api_key"),  # optional if stored in config.json
#     )

#     # Choose voice manager based on config["mode"]
#     mode = config.get("mode", "hybrid").lower()
#     api_key = config.get("openai_api_key")

#     if mode in ["gpt", "hybrid"]:
#         print("🔊 Using GPT-powered voice assistant")
#         voice_manager = VoiceManagerGPT(
#             api_key=api_key,
#             wake_word=config.get("wake_word", "hey chef"),
#             voice=config.get("voice", "alloy"),
#             command_timeout=config.get("command_timeout", 10),
#         )
#     else:
#         print("🔊 Using LOCAL voice assistant (pyttsx3 + SpeechRecognition)")
#         voice_manager = VoiceManagerLocal(
#             wake_word=config.get("wake_word", "hey chef"),
#             command_timeout=config.get("command_timeout", 10),
#         )

#     # Setup cooking session + UI
#     session = CookingSession(recipe_manager, voice_manager)
#     ui = UIManager(root, recipe_manager, session)

#     # Run voice assistant in background thread
#     threading.Thread(
#         target=handle_voice_commands, args=(session, voice_manager), daemon=True
#     ).start()

#     root.deiconify()
#     root.mainloop()


# if __name__ == "__main__":
# main()

# Version 3:
# import tkinter as tk
# import threading
# import re

# from recipe_manager import RecipeManager
# from cooking_session import CookingSession
# from ui_manager import UIManager
# from utils import load_config
# from voice_manager_gpt import VoiceManagerGPT
# from voice_manager_local import VoiceManagerLocal


# def normalize(s):
#     return re.sub(r"[^a-z0-9 ]+", "", s.lower()).strip()


# def match_recipe_title(text, titles):
#     t = normalize(text)
#     for title in titles:
#         nt = normalize(title)
#         if t == nt or t in nt or nt in t:
#             return title
#     return None


# def handle_voice_commands(root, ui, recipe_manager, session, voice_manager):
#     TITLES = [r["title"] for r in recipe_manager.recipes]

#     def set_ui(text, color="gray"):
#         root.after(0, lambda: ui.set_status(text, color))

#     def set_step(text):
#         root.after(0, lambda: ui.step_label.config(text=text))

#     while True:
#         set_ui("Listening for wake word…", "green")
#         cmd = voice_manager.wait_for_wake_word()
#         set_ui("Processing…", "orange")
#         print("Command received:", cmd)

#         if cmd in {"start", "next", "repeat", "clarify", "switch_step", "switch_all"}:
#             if cmd == "start":
#                 out = session.start("step")
#                 set_step(out if isinstance(out, str) else "\n".join(out))
#             elif cmd == "next":
#                 set_step(session.next_step())
#             elif cmd == "repeat":
#                 set_step(session.repeat_step())
#             elif cmd == "clarify":
#                 set_step(session.clarify_step())
#             elif cmd == "switch_step":
#                 set_step(session.start("step"))
#             elif cmd == "switch_all":
#                 out = session.start("all")
#                 set_step(out if isinstance(out, str) else "\n".join(out))
#             set_ui("Ready", "gray")
#             continue

#         title = match_recipe_title(cmd, TITLES)
#         if title:
#             recipe_manager.select_by_title(title)
#             root.after(0, ui.refresh_loaded_recipe)
#             voice_manager.speak(f"Loaded {title}. Say start when you're ready.")
#             set_step(f"🍳 Recipe selected: {title}\nSay 'start' or press ▶️ Start.")
#             set_ui("Ready", "gray")
#             continue

#         voice_manager.speak(
#             "Sorry, I didn't catch that. Say a recipe name, or say start, next, repeat, or clarify."
#         )
#         set_step("❓ Try: 'Scrambled Eggs', 'Start', 'Next', 'Repeat', or 'Clarify'.")
#         set_ui("Ready", "gray")


# def main():
#     cfg = load_config()
#     root = tk.Tk()
#     root.withdraw()

#     recipe_manager = RecipeManager("recipes.json", api_key=cfg.get("openai_api_key"))

#     # ✅ Get API key safely
#     openai_api_key = cfg.get("openai_api_key") or os.getenv("OPENAI_API_KEY")

#     # ✅ Default to GPT if mode not specified
#     mode = cfg.get("mode", "gpt").lower()

#     # ✅ Gracefully handle GPT vs Local mode
#     if mode in ["gpt", "hybrid"] and openai_api_key:
#         print("🔊 Using GPT-powered voice assistant")
#         vm = VoiceManagerGPT(
#             api_key=openai_api_key,
#             voice=cfg.get("voice", "alloy"),
#             wake_word=cfg.get("wake_word", "hey chef"),
#             command_timeout=cfg.get("command_timeout", 10),
#             config=cfg,
#         )
#     else:
#         if not openai_api_key:
#             print("⚠️ No OpenAI API key found. Falling back to LOCAL mode.")
#         else:
#             print("🔊 Using LOCAL voice assistant")

#         vm = VoiceManagerLocal(
#             wake_word=cfg.get("wake_word", "hey chef"),
#             command_timeout=cfg.get("command_timeout", 10),
#         )

#     # ✅ Initialize the cooking session and UI
#     session = CookingSession(recipe_manager, vm)
#     ui = UIManager(root, recipe_manager, session)

#     # ✅ Run voice assistant in a background thread
#     threading.Thread(
#         target=handle_voice_commands,
#         args=(root, ui, recipe_manager, session, vm),
#         daemon=True,
#     ).start()

#     root.deiconify()
#     root.mainloop()

# if __name__ == "__main__":
#     main()

import tkinter as tk, threading, re, os
from difflib import get_close_matches

from recipe_manager import RecipeManager
from cooking_session import CookingSession
from ui_manager import UIManager
from utils import load_config
from voice_manager_gpt import VoiceManagerGPT
from voice_manager_local import VoiceManagerLocal


def normalize(s):
    return re.sub(r"[^a-z0-9 ]+", "", (s or "").lower()).strip()


def match_recipe_title(text, titles):
    t = normalize(text)
    if not t:
        return None
    normalized = {normalize(tt): tt for tt in titles}
    # try direct contains
    for k, original in normalized.items():
        if t == k or t in k or k in t:
            return original
    # fuzzy
    close = get_close_matches(t, list(normalized.keys()), n=1, cutoff=0.55)
    return normalized[close[0]] if close else None


def handle_voice_commands(root, ui, recipe_manager, session, voice_manager):
    def set_ui(text, color="gray"):
        root.after(0, lambda: ui.set_status(text, color))

    def set_step(text):
        root.after(0, lambda: ui.step_label.config(text=text))

    while True:
        set_ui("Listening for wake word…", "green")
        cmd = voice_manager.wait_for_wake_word()
        set_ui("Processing…", "orange")
        print("Command received:", cmd)

        # Flow commands
        if cmd in {"start", "next", "repeat", "clarify", "switch_step", "switch_all"}:
            if not recipe_manager.current and cmd != "start":
                voice_manager.speak("Please select a recipe first.")
                set_step("⚠️ Please select a recipe first.")
                set_ui("Ready", "gray")
                continue

            if cmd == "start":
                out = session.start("step")
                set_step(out if isinstance(out, str) else "\n".join(out))
            elif cmd == "next":
                set_step(session.next_step())
            elif cmd == "repeat":
                set_step(session.repeat_step())
            elif cmd == "clarify":
                set_step(session.clarify_step())
            elif cmd == "switch_step":
                set_step(session.start("step"))
            elif cmd == "switch_all":
                out = session.start("all")
                set_step(out if isinstance(out, str) else "\n".join(out))
            set_ui("Ready", "gray")
            continue

        # Try to load by voice title
        titles = recipe_manager.get_titles()
        title = match_recipe_title(cmd, titles)
        if title:

            def bg():
                recipe = recipe_manager.select_by_title(title)
                if recipe:
                    root.after(0, lambda: ui.recipe_var.set(title))
                    root.after(0, ui.refresh_loaded_recipe)
                    voice_manager.speak(f"Loaded {title}. Say start when you're ready.")
                    set_step(
                        f"🍳 Recipe selected: {title}\nSay 'start' or press ▶️ Start."
                    )
                set_ui("Ready", "gray")

            threading.Thread(target=bg, daemon=True).start()
            continue

        # Fallback
        voice_manager.speak(
            "Say a recipe name, or say start, next, repeat, or clarify."
        )
        set_step("❓ Try: 'Tuna Salad', 'Start', 'Next', 'Repeat', or 'Clarify'.")
        set_ui("Ready", "gray")


def main():
    cfg = load_config()
    root = tk.Tk()
    root.withdraw()

    recipe_manager = RecipeManager("recipes.json", api_key=cfg.get("openai_api_key"))

    api_key = cfg.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    mode = (cfg.get("mode") or "gpt").lower()
    if mode in ["gpt", "hybrid"] and api_key:
        print("🔊 Using GPT-powered voice assistant")
        vm = VoiceManagerGPT(
            api_key=api_key,
            voice=cfg.get("voice", "alloy"),
            wake_word=cfg.get("wake_word", "hey chef"),
            command_timeout=cfg.get("command_timeout", 10),
            config=cfg,
        )
    else:
        if not api_key:
            print("⚠️ No OpenAI API key found. Falling back to LOCAL mode.")
        else:
            print("🔊 Using LOCAL voice assistant")
        from voice_manager_local import VoiceManagerLocal

        vm = VoiceManagerLocal(
            wake_word=cfg.get("wake_word", "hey chef"),
            command_timeout=cfg.get("command_timeout", 10),
        )

    session = CookingSession(recipe_manager, vm)
    ui = UIManager(root, recipe_manager, session)
    ui.refresh_recipe_dropdown()

    threading.Thread(
        target=handle_voice_commands,
        args=(root, ui, recipe_manager, session, vm),
        daemon=True,
    ).start()

    root.deiconify()
    root.mainloop()


if __name__ == "__main__":
    main()
