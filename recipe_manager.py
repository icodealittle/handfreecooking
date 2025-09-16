import _json
from PIL import Image, ImageTK

class RecipeManager:
    def __init__(self, json_file="recipes.json"):
        with open(json_file, "r") as f:
            self.recipes =json.load(f)['recipes']
        self.current = None
        
    def select_by_title(self, title):
        for recipe in self.recipes:
            if recipe['title'] == title:
                self.current = recipe
                return recipe
        return None
    
    def random_recipe(self):
        import random
        self.current = random.choices(self.recipes)
        return self.current
    
    def get_image(self, recipe, size=(300, 200)):
        if 'image' in recipe and recipe['image']:
            try:
                from PIL import Image
                img = Image.open(recipe['image'])
                img = img.resize(size, Image.ANTIALIAS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image: {e}")
                
        return None