import requests
import json


# Replace 'YOUR_API_KEY' with your actual Spoonacular API key
api_key = "55082fcb702947a5ac1b112e2c58baab"
# base_url = 'https://api.spoonacular.com/food/products/search'

# Request a list of diets
diets = ["pescetarian", "primal", "whole30"]

# Create lists to store all recipes and nutrition data
all_recipes = []


for diet in diets:
    recipes_url = "https://api.spoonacular.com/recipes/complexSearch"
    recipes_params = {
        "apiKey": api_key,
        "diet": diet,
        "number": 300,
    }  # Adjust the number of recipes as needed
    recipes_response = requests.get(recipes_url, params=recipes_params)

    if recipes_response.status_code == 200:
        recipes_data = recipes_response.json()
        print(f"\nRecipes for Diet: {diet.capitalize()}:")

        for result in recipes_data["results"]:
            # Extract relevant information for each recipe
            recipe_info = {
                "diet": diet.capitalize(),
                "title": result["title"],
                "recipe_id": result["id"],
            }
            all_recipes.append(recipe_info)
            print(json.dumps({"recipes": [recipe_info]}, indent=2))
else:
    print(
        f"Failed to get recipes for Diet: {diet.capitalize()}. Status code: {recipes_response.status_code}"
    )


output_data = {
    "recipes": all_recipes,
}
json_file_path = "Spoonacular_Recipe_feb3_p1.json"  # Change file name to perference.

# Save to JSON
with open(json_file_path, "w") as json_file:
    json.dump(output_data, json_file, indent=2)
print(f"Data saved to '{json_file_path}'")
