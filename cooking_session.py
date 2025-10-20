class CookingSession:
    """Controls cooking flow & speaks via voice_manager."""

    def __init__(self, recipe_manager, voice_manager):
        self.recipe_manager = recipe_manager
        self.voice_manager = voice_manager
        self.mode = "step"
        self.current_step = 0

    def _ensure_recipe(self):
        if not self.recipe_manager.current:
            self.voice_manager.speak("Please select a recipe first.")
            return False
        return True

    def start(self, mode="step"):
        if not self._ensure_recipe():
            return "⚠️ Please select a recipe first."
        self.mode = mode
        self.current_step = 0
        return self.read_step() if mode == "step" else self.read_all()

    def read_step(self):
        if not self._ensure_recipe():
            return "⚠️ Please select a recipe first."
        steps = self.recipe_manager.current.get("steps", [])
        if not steps:
            return "No steps found for this recipe."
        step = steps[self.current_step]
        self.voice_manager.speak(step)
        return f"Step {self.current_step+1}/{len(steps)}:\n{step}"

    def next_step(self):
        if not self._ensure_recipe():
            return "⚠️ Please select a recipe first."
        steps = self.recipe_manager.current.get("steps", [])
        if not steps:
            return "No steps found for this recipe."
        if self.current_step < len(steps) - 1:
            self.current_step += 1
        return self.read_step()

    def repeat_step(self):
        if not self._ensure_recipe():
            return "⚠️ Please select a recipe first."
        return self.read_step()

    def clarify_step(self):
        if not self._ensure_recipe():
            return "⚠️ Please select a recipe first."
        clar = self.recipe_manager.current.get("clarifications", [])
        if self.current_step < len(clar) and clar[self.current_step]:
            tip = clar[self.current_step]
        else:
            tip = "Tip: go slow and keep an eye on heat."
        self.voice_manager.speak(tip)
        return tip

    def read_all(self):
        if not self._ensure_recipe():
            return "⚠️ Please select a recipe first."
        steps = self.recipe_manager.current.get("steps", [])
        if not steps:
            return "No steps found for this recipe."
        text = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        self.voice_manager.speak("Starting recipe. I'll read the steps for you.")
        return text
