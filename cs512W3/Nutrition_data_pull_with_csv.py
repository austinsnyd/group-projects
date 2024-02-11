import requests
import csv
import json
import os

# This file is for pulling nutritional data for each recipe on the csv file

# Replace 'YOUR_API_KEY' with your actual Spoonacular API key
api_key = "8a7d3d5f77104bf3814130f149bd1a6f"


# Print the current working directory
# print("Current working directory:", os.getcwd())

# Print the current working directory
# os.chdir(r"C:\Users\hsmit\Desktop\OSU\CS512\Assignments\Data Wanger")# Path to work directory
# print("chdir 1:", os.getcwd())

# Specify the correct file path based on your working directory
csv_file_path = "Recipes_feb3.csv"

# Load data from CSV
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    diet_recipe_data = list(csv_reader)

# Create lists to store all recipes and nutrition data
all_recipe_data = []
all_nutrition_data = []

for index, row in enumerate(
    diet_recipe_data[:50]
):  # limits data pulling to first 50 rows
    # change to: for row in diet_recipe_data: to pull all rows in csv, becareful of points
    diet = row["diet"]
    title = row["title"]
    recipe_id = row["recipe_id"]

    # Fetch recipe information from the CSV
    recipe_info = {"Diet": diet, "Title": title, "Recipe_id": recipe_id}
    all_recipe_data.append(recipe_info)

    # Step 2: Fetch nutrition facts for each recipe
    nutrition_url = (
        f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    )
    nutrition_params = {"apiKey": api_key}
    nutrition_response = requests.get(nutrition_url, params=nutrition_params)

    if nutrition_response.status_code == 200:
        nutrition_data = nutrition_response.json()

        # Separate Nutrients and ingredients data
        nutrients_data = nutrition_data.get("nutrients", [])

        all_nutrition_data.append({"recipe_id": recipe_id, "nutrients": nutrition_data})
    else:
        print(
            f"Failed to get nutrition facts for Recipe ID {recipe_id}. Status code: {nutrition_response.status_code}"
        )


output_data = {
    "recipes_data": all_recipe_data,
    "nutrition_data": all_nutrition_data,
    # "price_breakdown_data": all_price_breakdown_data
}
json_file_path = "Nutrition_feb3"  # Change file name to perference.

# Save to JSON
with open(json_file_path, "w") as json_file:
    json.dump(output_data, json_file, indent=2)
print(f"Data saved to '{json_file_path}'")
