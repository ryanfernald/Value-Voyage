import pandas as pd

# Load the CSV file
df = pd.read_csv("/Users/xewe-code/Desktop/housing_1953-2024/adjusted.csv")

# Convert 'date' to datetime and extract year and month
df.rename(columns={"category": "date"}, inplace=True)
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.strftime('%b')  # Jan, Feb, etc.

# Pivot the DataFrame
pivot_df = df.pivot(index='year', columns='month', values='price').reset_index()

# Save to CSV
pivot_df.to_csv("/Users/xewe-code/Desktop/housing_1953-2024/adjusted_pivoted_output.csv", index=False)
