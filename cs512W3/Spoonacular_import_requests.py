import requests
import csv
import json
import pandas as pd



# Replace 'YOUR_API_KEY' with your actual Spoonacular API key
api_key = 'e94f4e6b04ba4032bb464cd67015ce54'
# base_url = 'https://api.spoonacular.com/food/products/search'

# Request a list of diets
diets = ['vegetarian', 'ketogenic', 'vegan', 'gluten free']

# Create lists to store all recipes and nutrition data
all_recipes = []
all_nutrition_data = []
all_diet_recipes = []
all_price_breakdown_data = []

for diet in diets:
    recipes_url = 'https://api.spoonacular.com/recipes/complexSearch'
    recipes_params = {'apiKey': api_key, 'diet': diet, 'number': 300}  # Adjust the number of recipes as needed
    recipes_response = requests.get(recipes_url, params=recipes_params)

    if recipes_response.status_code == 200:
        recipes_data = recipes_response.json()
        print(f"\nRecipes for Diet: {diet.capitalize()}:")
        
        for result in recipes_data['results']:
            info = (f"{diet.capitalize()} - {result['title']} - {result['id']}")
            print(info)
            all_diet_recipes.append(info)

    # Step 2: Fetch nutrition facts for each recipe
        nutrition_url = f'https://api.spoonacular.com/recipes/{result["id"]}/nutritionWidget.json'
        nutrition_params = {'apiKey': api_key}
        nutrition_response = requests.get(nutrition_url, params=nutrition_params)

        if nutrition_response.status_code == 200:
            nutrition_data = nutrition_response.json()

            # Separate Nutrients and ingredients data
            nutrients_data = nutrition_data.get("nutrients", [])

            all_nutrition_data.append({"recipe_id": result["id"], "nutrients": nutrition_data})

            # Step 3: Fetch price breakdown for each recipe ingredient

            price_breakdown_url = f'https://api.spoonacular.com/recipes/{result["id"]}/priceBreakdownWidget.json'
            price_breakdown_params = {'apiKey': api_key}
            price_breakdown_response = requests.get(price_breakdown_url, params=price_breakdown_params)

            if price_breakdown_response.status_code == 200:
                price_breakdown_data = price_breakdown_response.json()
                price_data = price_breakdown_data.get("ingredients", [])
                
                # Append the extracted information to the list
                all_price_breakdown_data.append({"recipe_id": result["id"], "name": price_breakdown_data, "price": price_breakdown_data})
            else:
                    print(f"Failed to get price breakdown for Recipe ID {result['id']}. Status code: {price_breakdown_response.status_code}")
        else:
            print(f"Failed to get nutrition facts for Recipe ID {result['id']}. Status code: {nutrition_response.status_code}")
    else:
        print(f"Failed to get recipes for Diet: {diet.capitalize()}. Status code: {recipes_response.status_code}")





output_data = {
"recipes": all_diet_recipes,
"nutrition_data": all_nutrition_data,
"price_breakdown_data": all_price_breakdown_data
}    
json_file_path = 'Spoonacular_data_pull.json' # Change file name to perference. 

# Save to JSON
with open(json_file_path, 'w') as json_file:
    json.dump(output_data, json_file, indent=2)
print(f"Data saved to '{json_file_path}'")


