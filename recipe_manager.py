import json
import os
import random
from openai import OpenAI
from PIL import Image, ImageTk

class RecipeManager:
    """Manages recipes, including loading from a JSON file, fetching new recipes from GPT, caching them,
    and providing cooking tips for recipe steps."""
    
    def __init__(self, json_file = "recipes.json", api_key = None):
        self.json_file = json_file
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                self.recipes = json.load(f)['recipes']
        else:
            self.recipes = []
        
        self.current = None
        
        """Select recipe by title form local JSON
        """
    def select_by_title(self, title):
        for recipe in self.recipes:
            if recipe['title'] == title:
                self.current = recipe
                return recipe
        return None
    
    """Pick a random recipe from local JSON"""
    def random_recipe(self):
        self.current = random.choice(self.recipes) if self.recipes else None
        return self.current
    
    """Fetch a new recipe from GPT based on a query string, if not found locally"""
    def fetch_recipe_from_gpt(self, query):
        prompt = f"""
        Find a simple recipe for {query}.
        Return the recipe in the following JSON format:
        {{
            "title": "...",
            "ingredients": ["..."],
            "steps": ["..."],
            "clarificatoin": ["Tip:....", "Tip:..."]
            }}
            """
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini", messages=[{"role": "system", "content": "You are a cooking assistant that only outputs valid JSON recipes."},
                {"role": "user", "content": prompt}
            ]
        )
        
        recipe_json = response.choices[0].message.content.strip()
        try:
            recipe = json.loads(recipe_json)
            self.current = recipe
            self._cache_recipe(recipe)
            return recipe
        except Exception as e:
            print("Failed to parse recipe JSON:", e)
            return None
    
    """Get a cooking tip for a specific step in the current recipe, generating it via GPT if not cached"""
    def get_clarification(self, step_index):
        if not self.current:
            return "No recipe loaded."
            
        clarifications = self.current.get("clarifications", [])
        if step_index < len(clarifications):
            return clarifications[step_index]
            
        step_text = self.current['steps'][step_index]
        prompt = f"""
            Give a helpful cooking tip for this step: "{step_text}". Return only one short tip starting with "Tip:".
            """
            
        try:
            response = self.client.chat.completions.create(
                    model="gpt-4.1-mini", messages=[{"role": "system", "content": "You are a cooking assistant that provides helpful cooking tips."},
                        {"role": "user", "content": prompt}
                    ]
                )
            tip = response.choices[0].message.content.strip()
            if "clarifications" not in self.current:
                self.current["clarifications"] = []
            while len(self.current["clarifications"]) <= step_index:
                self.current["clarifications"].append("")
            self.current["clarifications"][step_index] = tip
            self._cache_recipe(self.current)
            return tip
        except:
            return "Sorry, i don't have a tip right now."

    """Save recipe to local JSON cache"""
    def _cache_recipe(self, recipe):
        titles = [r["title"].lower() for r in self.recipes]
        if recipe['title'].lower() not in titles:
            self.recipes.append(recipe)
        else:
            for i, r in enumerate(self.recipes):
                if r["title"].lower() == recipe["title"].lower():
                    self.recipes[i] = recipe
        with open(self.json_file, 'w') as f:
            json.dump({"recipes": self.recipes}, f, indent=4)
    
    """Return a resized image for the recipe if available"""
    def get_image(self, recipe, size=(300, 200)):
        if 'image' in recipe and recipe['image']:
            try:
                image = Image.open(recipe['image'])
                image = image.resize(size, Image.ANTIALIAS)
                return ImageTk.PhotoImage(image)
            except:
                return None
        return None