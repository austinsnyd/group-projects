import os
import csv
import json

def csv_to_json(csv_file):
    data = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def main(folder_path, output_file):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return
    
    json_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_file = os.path.join(folder_path, filename)
            print(f"Processing {csv_file}")
            json_data[filename] = csv_to_json(csv_file)

    with open(output_file, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

if __name__ == "__main__":
    folder_path = r'C:\Users\hsmit\Desktop\OSU\CS512\Assignments\Data Wrangling\FoodData_Central_csv_2023-10-26'
    output_file = 'FoodData_Central.json'
    main(folder_path, output_file)