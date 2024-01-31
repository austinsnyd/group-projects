import pandas as pd

# Read the CSV file
df = pd.read_csv('/Users/austinsnyder/school/cs512W3/Data_Wrangler.csv')

# Export the DataFrame to an Excel file
df.to_excel('/Users/austinsnyder/school/cs512W3/Data_Wrangler.xlsx', index=False)
