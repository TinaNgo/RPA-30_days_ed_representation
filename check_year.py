import pandas as pd

# Load your dataset (replace 'your_file.csv' with your actual file path)
df = pd.read_csv("truncated.csv")

# Ensure the 'arrival_date' column is in datetime format (replace 'arrival_date' with your actual date column name)
df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')

# Drop rows with invalid or missing dates
df = df.dropna(subset=['arrival_date'])

df['year'] = df['arrival_date'].dt.year

# Find the minimum and maximum year
min_year = df['year'].min()
max_year = df['year'].max()

# Print the year range
print(f"The dataset contains records from the year {min_year} to {max_year}.")