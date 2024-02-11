import pandas as pd
import sqlite3


def import_csv_to_table(csv_file_path, table_name, db_name, schema=None):
    """
    Imports a CSV file into a SQLite table.

    Parameters:
    - csv_file_path: Path to the CSV file.
    - table_name: Name of the table in the SQLite database.
    - db_name: Name of the SQLite database.
    - schema: Schema of the table if creating for the first time.
    """
    conn = sqlite3.connect(db_name)

    # If schema is provided, use it to create the table
    if schema:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")

    df = pd.read_csv(csv_file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()


def main():
    db_name = "diet_data.db"

    # Define your tables, CSV files, and schema
    tables = {
        "recipes": (
            "Data_Wrangling_Recipes_for_Diet.csv",
            "diet TEXT, title TEXT, recipe_id INTEGER",
        ),
        "nutrition": (
            "Data_wrangling_recipe_nutrition.csv",
            "recipe_id INTEGER, calories INTEGER, carbs TEXT, fat TEXT, protein TEXT",
        ),
    }

    for table_name, (csv_file, schema) in tables.items():
        import_csv_to_table(csv_file, table_name, db_name, schema=schema)
        print(f"Imported {csv_file} into {table_name}")

    # Example of joining the tables using SQL
    conn = sqlite3.connect(db_name)
    query = """
    SELECT a.*, b.calories, b.carbs, b.fat, b.protein
    FROM recipes a
    JOIN nutrition b ON a.recipe_id = b.recipe_id
    """
    joined_data = pd.read_sql_query(query, conn)
    print(joined_data.head())  # Prints the first 10 rows of the joined table
    conn.close()


if __name__ == "__main__":
    main()
