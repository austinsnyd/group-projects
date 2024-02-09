import json
import csv


class Diet:
    def __init__(self, diet, title, recipe_id):
        self.diet = diet
        self.title = title
        self.recipe_id = recipe_id


class Recipe:
    def __init__(self, recipe_id, nutrients, ingredients):
        self.recipe_id = recipe_id
        self.nutrients = nutrients
        self.ingredients = ingredients

    @classmethod
    def from_json(cls, json_data):
        recipe_id = json_data.get("recipe_id", "")
        nutrients_data = json_data.get("nutrients", {})
        ingredients_data = nutrients_data.get("ingredients", [])

        ingredients = [
            {
                "name": ingredient.get("name", ""),
                "amount": ingredient.get("amount", 0),
                "unit": ingredient.get("unit", ""),
                "id": ingredient.get("id", ""),
            }
            for ingredient in ingredients_data
        ]

        nutrients = {
            "calories": nutrients_data.get("calories", ""),
            "carbs": nutrients_data.get("carbs", ""),
            "fat": nutrients_data.get("fat", ""),
            "protein": nutrients_data.get("protein", ""),
        }
        return cls(recipe_id, nutrients, ingredients)

    @classmethod
    def extract_nutrition_info(cls, nutrition_data):
        extracted_info = []
        for entry in nutrition_data:

            recipe_id = entry.get("recipe_id", "")
            nutrients_data = entry.get("nutrients", {})

            # Extract specific nutrient values
            nutrients = {
                "calories": nutrients_data.get("calories", ""),
                "carbs": nutrients_data.get("carbs", ""),
                "fat": nutrients_data.get("fat", ""),
                "protein": nutrients_data.get("protein", ""),
            }

            recipe = cls(recipe_id, nutrients)
            extracted_info.append(recipe)

        return extracted_info

    @classmethod
    def extract_ingredients_info(cls, nutrition_data):
        extracted_info = []

        for entry in nutrition_data:
            recipe_id = entry.get("recipe_id", "")
            nutrients_data = entry.get("nutrients", {})
            ingredients_data = nutrients_data.get("ingredients", [])

            ingredients = [
                {
                    "name": ingredient.get("name", ""),
                    "amount": ingredient.get("amount", 0),
                    "unit": ingredient.get("unit", ""),
                    "id": ingredient.get("id", ""),
                }
                for ingredient in ingredients_data
            ]

            recipe = cls(recipe_id, nutrients_data, ingredients)
            extracted_info.append(recipe)

        return extracted_info


class RecipePrice:
    def __init__(self, recipe_id, name, price):
        self.recipe_id = recipe_id
        self.name = name
        self.price = price


# Load data

# with open('Spoonacular_data_pull.json', 'r') as spoonacular_data_pull:
with open("Nutrition_feb3", "r") as spoonacular_data_pull:
    diet_data = json.load(spoonacular_data_pull)

# Parse and create Diet objects

# Create a dictionary to store nutrition data with recipe ID as the key
nutrition_data_dict = {
    entry["recipe_id"]: entry for entry in diet_data.get("nutrition_data", [])
}

diet_objects = []


for entry in diet_data["recipes_data"]:

    diet = entry["Diet"]
    # title = entry.get("Title", "No Title") Was used if data has no title
    title = entry["Title"]
    recipe_id = entry["Recipe_id"]

    # Create Diet object
    diet_objects.append(Diet(diet, title, recipe_id))

# Create Recipe objects

# Get nutrition data from the dictionary based on recipe ID
nutrition_entry = nutrition_data_dict.get(recipe_id, {}).get("nutrients", {})
# Extract specific nutrient values
nutrients = {
    "calories": nutrition_entry.get("calories", ""),
    "carbs": nutrition_entry.get("carbs", ""),
    "fat": nutrition_entry.get("fat", ""),
    "protein": nutrition_entry.get("protein", ""),
}


# Create Recipe object with nutrients
recipe_objects = []
recipe = Recipe(recipe_id, nutrients, [])

# Append the Recipe object to the list
recipe_objects.append(recipe)


# Create Ingredient objects
ingredient_objects = Recipe.extract_ingredients_info(
    diet_data.get("nutrition_data", [])
)

# Write to SQL Table

# Write data to CSV
with open("nutrition_data_pull_feb3.csv", "w", newline="") as csvfile:
    # Write the first sheet
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ["diet", "title", "recipe_id", "calories", "carbs", "fat", "protein"]
    )
    for diet_obj in diet_objects:
        nutrition_entry = nutrition_data_dict.get(diet_obj.recipe_id, {})
        nutrients = nutrition_entry.get("nutrients", {})

        # Write row with diet_obj information and corresponding nutrition data
        csv_writer.writerow(
            [
                diet_obj.diet,
                diet_obj.title,
                diet_obj.recipe_id,
                nutrients.get("calories", ""),
                nutrients.get("carbs", ""),
                nutrients.get("fat", ""),
                nutrients.get("protein", ""),
            ]
        )
