import os
import pandas as pd
import mysql.connector

def import_csv_to_table(csv_file_path, table_name, conn, csv_file, failed_files):
    """
    Imports a CSV file into a MySQL table.

    Parameters:
    - csv_file_path: Path to the CSV file.
    - table_name: Name of the table in the MySQL database.
    - conn: MySQL connection object.
    - schema: Schema of the table if creating for the first time.
    """
    cursor = conn.cursor()
    success = False
    try:
        # Read the CSV file to infer column data types
        df = pd.read_csv(csv_file_path, nrows=100)  # Read the first 100 rows for inference

        default_values = {col: 0 if df[col].dtype == 'float64' else '' for col in df.columns}
        df.fillna(default_values, inplace=True)  # Replace NaNs with 0 for numerical columns and '' for string columns

        columns = df.columns
        dtypes = df.dtypes

        # Map pandas data types to MySQL data types
        type_mapping = {
            'int64': 'INT',
            'float64': 'FLOAT',
            'object': 'TEXT'  # Assuming all other types as TEXT
        }

        # Construct the schema based on inferred data types
        schema = ', '.join([f"{col} {type_mapping[str(dtype)]}" for col, dtype in zip(columns, dtypes)])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")

        # Read the entire CSV file (without nrows limit) for data insertion
        df = pd.read_csv(csv_file_path)

        for _, row in df.iterrows():
            sql_values = ', '.join(map(repr, row.values))
            sql = f"INSERT INTO {table_name} VALUES ({sql_values})"
            cursor.execute(sql)

        conn.commit()
        print(f"Imported {csv_file} into table {table_name}")

    except Exception as e:
        print(f"Failed to import {csv_file}: {e}")
        failed_files.append(csv_file_path)

    finally:
        cursor.close()
        return success

def main():
    db_name = "cs512"
    failed_files = []

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="DESKTOP-HANNAH",
        user="Hannah",
        password="PK146JJhs_p8",
        database=db_name
    )

    # Specify the folder path containing CSV files
    folder_path = r'C:\Users\hsmit\Desktop\OSU\CS512\Assignments\Data Wrangling\FoodData_Central_csv_2023-10-26'

    # Get a list of all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Import each CSV file into a table named after the CSV file
    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]
        csv_file_path = os.path.join(folder_path, csv_file)
        success = import_csv_to_table(csv_file_path, table_name, conn, csv_file, failed_files)
        if success:
            print(f"Imported {csv_file} into table {table_name}")
        else:
            print(f"Skipping {csv_file} due to import failure.")

    # Close the connection
    conn.close()
    # Print the list of failed files
    if failed_files:
        print("List of failed files:")
        for file in failed_files:
            print(file)
    else:
        print("All files imported successfully.")
if __name__ == "__main__":
    main()