import tkinter as tk
from tkinter import ttk
from utils import log_event, load_config

class UIManager:

    # Initialize the UI manager with the main window, recipe manager, and cooking session.
    def __init__(self, root, recipe_manager, session):
        self.root = root
        self.recipe_manager = recipe_manager
        self.session = session

        root.title("Hand-free Cooking Assistant")
        root.geometry("800x600")

        self.app_title = tk.Label(
            root, text="👩‍🍳 Hand-free Cooking", font=("Arial", 20, "bold")
        )
        self.app_title.pack(pady=10)

        self.recipe_var = tk.StringVar(root)
        recipe_titles = [r["title"] for r in recipe_manager.recipes]
        self.recipe_dropdown = ttk.Combobox(
            root, textvariable=self.recipe_var, values=recipe_titles, state="readonly"
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
            root, text="", font=("Arial", 14), wraplength=600, justify="left"
        )
        self.step_label.pack(pady=10)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Button(
            control_frame, text="▶️ Start", command=lambda: self.start("step")
        ).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="➡️ Next", command=self.next_step).grid(
            row=0, column=1, padx=5
        )
        tk.Button(control_frame, text="🔁 Repeat", command=self.repeat_step).grid(
            row=0, column=2, padx=5
        )
        tk.Button(control_frame, text="💡 Clarify", command=self.clarify_step).grid(
            row=0, column=3, padx=5
        )

    # Load recipe from dropdown and display details
    def load_recipe_from_dropdown(self, event):
        title = self.recipe_var.get()
        recipe = self.recipe_manager.select_by_title(title)
        if recipe:
            self.recipe_title.config(text=recipe["title"])
            img = self.recipe_manager.get_image(recipe)
            if img:
                self.recipe_image_label.config(image=img)
                self.recipe_image_label.image = img
            log_event(f"Recipe loaded: {recipe['title']}")

    def start(self, mode="step"):
        text = self.session.start(mode)
        if isinstance(text, str):
            self.step_label.config(text=text)
        else:
            self.step_label.config(text="\n".join(text))

    def next_step(self):
        text = self.session.next_step()
        if text:
            self.step_label.config(text=text)

    def repeat_step(self):
        text = self.session.repeat_step()
        self.step_label.config(text=text)

    def clarify_step(self):
        tip = self.session.clarify_step()
        self.step_label.config(text=f"Clarification: {tip}")
