import json, os, random
from PIL import Image, ImageTk


class RecipeManager:
    """Loads & manages recipes from a JSON file. Keeps `current` in sync."""

    def __init__(self, json_file="recipes.json", api_key=None):
        self.json_file = json_file
        self.recipes = []
        self.current = None
        self._load_recipes()

    # ---------- load/cache ----------
    def _load_recipes(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as f:
                data = json.load(f)
                self.recipes = data.get("recipes", [])
        else:
            self.recipes = []

    def get_titles(self):
        return [r.get("title") or r.get("name") or "Untitled" for r in self.recipes]

    # ---------- selection ----------
    def select_by_title(self, title: str):
        if not title:
            self.current = None
            return None
        t = title.strip().lower()
        for r in self.recipes:
            rt = (r.get("title") or r.get("name") or "").strip().lower()
            if rt == t:
                self.current = r
                return r
        # fallback: loose contains
        for r in self.recipes:
            rt = (r.get("title") or r.get("name") or "").strip().lower()
            if t in rt or rt in t:
                self.current = r
                return r
        print(f"[WARN] Recipe '{title}' not found.")
        self.current = None
        return None

    def random_recipe(self):
        if not self.recipes:
            self.current = None
            return None
        self.current = random.choice(self.recipes)
        return self.current

    # ---------- assets ----------
    def get_image(self, recipe, size=(300, 200)):
        path = (recipe or {}).get("image")
        if not path:
            return None
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print("[IMG] load error:", e)
            return None
