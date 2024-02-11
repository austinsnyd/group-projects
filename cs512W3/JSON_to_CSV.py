import pandas as pd
import json


def json_to_csv(json_file_path, csv_file_path):
    # Load the JSON file
    with open(json_file_path, "r") as f:
        data = json.load(f)

    # Extract the recipes list from the loaded JSON data
    recipes = data["recipes"]

    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(recipes)

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)


def main():
    json_to_csv("Spoonacular_Recipe_feb3_p1.json", "Recipes_feb3.csv")


if __name__ == "__main__":
    main()
