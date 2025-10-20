# import tkinter as tk
# from tkinter import ttk
# from utils import log_event, load_config

# class UIManager:

#     # Initialize the UI manager with the main window, recipe manager, and cooking session.
#     def __init__(self, root, recipe_manager, session):
#         self.root = root
#         self.recipe_manager = recipe_manager
#         self.session = session

#         root.title("Hand-free Cooking Assistant")
#         root.geometry("800x600")

#         self.app_title = tk.Label(
#             root, text="👩‍🍳 Hand-free Cooking", font=("Arial", 20, "bold")
#         )
#         self.app_title.pack(pady=10)

#         self.recipe_var = tk.StringVar(root)
#         recipe_titles = [r["title"] for r in recipe_manager.recipes]
#         self.recipe_dropdown = ttk.Combobox(
#             root, textvariable=self.recipe_var, values=recipe_titles, state="readonly"
#         )
#         self.recipe_dropdown.set("Select Recipe")
#         self.recipe_dropdown.bind(
#             "<<ComboboxSelected>>", self.load_recipe_from_dropdown
#         )
#         self.recipe_dropdown.pack()

#         self.recipe_title = tk.Label(root, text="", font=("Arial", 18, "bold"))
#         self.recipe_title.pack(pady=10)

#         self.recipe_image_label = tk.Label(root)
#         self.recipe_image_label.pack()

#         self.step_label = tk.Label(
#             root, text="", font=("Arial", 14), wraplength=600, justify="left"
#         )
#         self.step_label.pack(pady=10)

#         control_frame = tk.Frame(root)
#         control_frame.pack(pady=10)

#         tk.Button(
#             control_frame, text="▶️ Start", command=lambda: self.start("step")
#         ).grid(row=0, column=0, padx=5)
#         tk.Button(control_frame, text="➡️ Next", command=self.next_step).grid(
#             row=0, column=1, padx=5
#         )
#         tk.Button(control_frame, text="🔁 Repeat", command=self.repeat_step).grid(
#             row=0, column=2, padx=5
#         )
#         tk.Button(control_frame, text="💡 Clarify", command=self.clarify_step).grid(
#             row=0, column=3, padx=5
#         )

#     # Load recipe from dropdown and display details
#     def load_recipe_from_dropdown(self, event):
#         title = self.recipe_var.get()
#         recipe = self.recipe_manager.select_by_title(title)
#         if recipe:
#             self.recipe_title.config(text=recipe["title"])
#             img = self.recipe_manager.get_image(recipe)
#             if img:
#                 self.recipe_image_label.config(image=img)
#                 self.recipe_image_label.image = img
#             log_event(f"Recipe loaded: {recipe['title']}")

#     def start(self, mode="step"):
#         if not self.recipe_manager.current:
#             self.step_label.config(text="Please select a recipe first.")
#             return

#         text = self.session.start(mode)
#         if isinstance(text, str):
#             self.step_label.config(text=text)
#         else:
#             self.step_label.config(text="\n".join(text))

#     def next_step(self):
#         text = self.session.next_step()
#         if text:
#             self.step_label.config(text=text)

#     def repeat_step(self):
#         text = self.session.repeat_step()
#         self.step_label.config(text=text)

#     def clarify_step(self):
#         tip = self.session.clarify_step()
#         self.step_label.config(text=f"Clarification: {tip}")

# version 2:
# import tkinter as tk
# from PIL import Image, ImageTk


# class UIManager:
#     def __init__(self, root, recipe_manager, session):
#         self.root = root
#         self.recipe_manager = recipe_manager
#         self.session = session

#         self.recipe_var = tk.StringVar(root)

#         # Build UI
#         self.build_ui()

#     def build_ui(self):
#         # Recipe dropdown
#         titles = self.recipe_manager.get_titles()
#         if titles:
#             self.recipe_dropdown = tk.OptionMenu(self.root, self.recipe_var, *titles)
#             self.recipe_dropdown.grid(row=0, column=0, padx=10, pady=10)

#             # 🔹 Bind selection to update recipe
#             self.recipe_var.trace_add("write", self.load_recipe_from_dropdown)

#         self.recipe_title = tk.Label(self.root, text="", font=("Arial", 16))
#         self.recipe_title.grid(row=1, column=0, columnspan=2, pady=10)

#         self.recipe_image_label = tk.Label(self.root)
#         self.recipe_image_label.grid(row=2, column=0, columnspan=2, pady=10)

#         self.step_label = tk.Label(
#             self.root, text="Select a recipe to begin", wraplength=400, justify="left"
#         )
#         self.step_label.grid(row=3, column=0, columnspan=2, pady=10)

#         control_frame = tk.Frame(self.root)
#         control_frame.grid(row=4, column=0, columnspan=2, pady=10)

#         tk.Button(
#             control_frame, text="▶️ Start", command=lambda: self.start("step")
#         ).grid(row=0, column=0, padx=5)
#         tk.Button(control_frame, text="⏭ Next", command=self.next_step).grid(
#             row=0, column=1, padx=5
#         )
#         tk.Button(control_frame, text="🔁 Repeat", command=self.repeat_step).grid(
#             row=0, column=2, padx=5
#         )
#         tk.Button(control_frame, text="❓ Clarify", command=self.clarify_step).grid(
#             row=0, column=3, padx=5
#         )

#     def load_recipe_from_dropdown(self, *args):
#         """Update the recipe when dropdown selection changes"""
#         title = self.recipe_var.get()
#         recipe = self.recipe_manager.select_by_title(title)
#         if recipe:
#             self.recipe_manager.current = recipe
#             self.recipe_title.config(text=recipe["title"])
#             img = self.recipe_manager.get_image(recipe)
#             if img:
#                 self.recipe_image_label.config(image=img)
#                 self.recipe_image_label.image = img
#             else:
#                 self.recipe_image_label.config(image="", text="")

#             self.step_label.config(text="Recipe loaded. Press ▶️ Start.")

#     def start(self, mode="step"):
#         """Start cooking session"""
#         if not self.recipe_manager.current:
#             self.step_label.config(text="⚠️ Please select a recipe first.")
#             return

#         text = self.session.start(mode)
#         if isinstance(text, str):
#             self.step_label.config(text=text)
#         elif isinstance(text, list):
#             self.step_label.config(text="\n".join(text))

#     def next_step(self):
#         text = self.session.next_step()
#         self.step_label.config(text=text)

#     def repeat_step(self):
#         text = self.session.repeat_step()
#         self.step_label.config(text=text)

#     def clarify_step(self):
#         text = self.session.clarify_step()
#         self.step_label.config(text=text)

# Version 3:
import tkinter as tk
from tkinter import ttk
from utils import log_event


class UIManager:
    def __init__(self, root, recipe_manager, session):
        self.root = root
        self.recipe_manager = recipe_manager
        self.session = session

        root.title("Hand-free Cooking Assistant")
        root.geometry("820x620")

        self.app_title = tk.Label(
            root, text="👩‍🍳 Hand-free Cooking", font=("Arial", 20, "bold")
        )
        self.app_title.pack(pady=10)

        # status
        self.status_label = tk.Label(root, text="Ready", fg="gray")
        self.status_label.pack()

        # recipe picker
        self.recipe_var = tk.StringVar(root)
        titles = [r["title"] for r in recipe_manager.recipes]
        self.recipe_dropdown = ttk.Combobox(
            root, textvariable=self.recipe_var, values=titles, state="readonly"
        )
        self.recipe_dropdown.set("Select Recipe")
        self.recipe_dropdown.bind(
            "<<ComboboxSelected>>", self.load_recipe_from_dropdown
        )
        self.recipe_dropdown.pack()

        self.recipe_title = tk.Label(root, text="", font=("Arial", 18, "bold"))
        self.recipe_title.pack(pady=10)

        self.recipe_image_label = tk.Label(root)
        self.recipe_image_label.pack()

        self.step_label = tk.Label(
            root, text="", font=("Arial", 14), wraplength=640, justify="left"
        )
        self.step_label.pack(pady=10)

        controls = tk.Frame(root)
        controls.pack(pady=10)

        tk.Button(controls, text="▶️ Start", command=lambda: self.start("step")).grid(
            row=0, column=0, padx=5
        )
        tk.Button(controls, text="⏭ Next", command=self.next_step).grid(
            row=0, column=1, padx=5
        )
        tk.Button(controls, text="🔁 Repeat", command=self.repeat_step).grid(
            row=0, column=2, padx=5
        )
        tk.Button(controls, text="💡 Clarify", command=self.clarify_step).grid(
            row=0, column=3, padx=5
        )
        tk.Button(
            controls, text="🛠 Calibrate my voice", command=self.calibrate_voice
        ).grid(row=0, column=4, padx=5)

    def set_status(self, text, color="gray"):
        self.status_label.config(text=text, fg=color)
        self.root.update_idletasks()

    def refresh_loaded_recipe(self):
        recipe = self.recipe_manager.current
        if recipe:
            self.recipe_title.config(text=recipe["title"])
            img = self.recipe_manager.get_image(recipe)
            if img:
                self.recipe_image_label.config(image=img)
                self.recipe_image_label.image = img

    def load_recipe_from_dropdown(self, _):
        title = self.recipe_var.get()
        recipe = self.recipe_manager.select_by_title(title)
        if recipe:
            log_event(f"Recipe loaded: {recipe['title']}")
            self.refresh_loaded_recipe()
            self.step_label.config(text="Recipe loaded. Say 'start' or press ▶️ Start.")

    def start(self, mode="step"):
        if not self.recipe_manager.current:
            self.step_label.config(text="⚠️ Please select a recipe first.")
            return
        out = self.session.start(mode)
        self.step_label.config(text=out if isinstance(out, str) else "\n".join(out))

    def next_step(self):
        self.step_label.config(text=self.session.next_step())

    def repeat_step(self):
        self.step_label.config(text=self.session.repeat_step())

    def clarify_step(self):
        self.step_label.config(text=self.session.clarify_step())

    def calibrate_voice(self):
        self.set_status("Calibrating…", "orange")
        try:
            self.session.voice_manager.calibrate(seconds=2)
        finally:
            self.set_status("Ready", "gray")
