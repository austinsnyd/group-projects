import json
import pandas as pd


def to_json():
    result = {}
    recipes = pd.read_csv("Data_Wrangling_Recipes_for_Diet.csv")
    nutrition = pd.read_csv("Data_wrangling_recipe_nutrition.csv")
    for _, recipe in recipes.iterrows():
        recipe_id = recipe["recipe_id"]
        result[recipe_id] = {
            "diet": recipe["diet"],
            "title": recipe["title"],
        }
    for _, nutrient in nutrition.iterrows():
        recipe_id = nutrient["recipe_id"]
        result[recipe_id].update(
            {
                "calories": nutrient["calories"],
                "carbs": nutrient["carbs"],
                "fat": nutrient["fat"],
                "protein": nutrient["protein"],
            }
        )
    with open("recipes.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    to_json()

# grabs data from both csv files
# iterates through the recipes csv file and grabs info
# iterates through the nutrition csv file and grabs info
# updates the result dictionary with the nutrition info
# saves the result dictionary to a json file
# outputs single JSON file, uses recipe id as key,
