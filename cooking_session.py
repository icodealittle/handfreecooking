from utils import log_event

"""Manages the cooking session, including reading steps, handling modes (step-by-step or all-at-once),
and interacting with the voice manager for TTS output."""
class CookingSession:
    def __init__(self, recipe_manager, voice_manager ):
        self.recipe_manager = recipe_manager
        self.voice_manager = voice_manager
        self.current_step = 0
        self.mode = None
    
    """Start the cooking session in the specified mode ('step' or 'all')"""
    def start(self, mode="step"):
        self.mode = mode
        self.current_step = 0
        log_event(f"Cooking started in {mode} mode.")
        if mode == 'step':
            return self.read_step()
        else:
            return self.read_all_steps()
    
    """Read the current step aloud and log it"""
    def read_step(self):
        step = self.recipe_manager.current['step'][self.current_step]
        text = f"Step {self.current_step + 1}: {step}"
        log_event(text)
        self.voice_manager.speak(text)
        return text
    
    """Advance to the next step, if available, and read it aloud"""
    def next_step(self):
        if self.current_step < len(self.recipe_manager.current['steps']) - 1:
            self.current_step += 1
            return self.read_step()
        else:
            log_event("Already at the last step.")
            return "You are already at the last step." 
    
    """Repeat the current step"""
    def repeat_step(self):
        return self.read_step()  
    
    """Get a clarification or tip for the current step"""
    def clarify_step(self):
        tip = self.recipe_manager.get_clarification(self.current_step)
        log_event(f"Clarification for step {self.current_step + 1}: {tip}")
        self.voice_manager.speak(tip)
        return tip
    
    """Read all steps aloud and log them"""
    def read_all_steps(self):
        all_steps = self.recipe_manager.current['steps']
        text = "Here are all the steps:\n" + "\n".join([f"Step {i+1}: {s}" for i, s in enumerate(all_steps)])
        log_event("Reading all steps.")
        self.voice_manager.speak(text)
        return text
