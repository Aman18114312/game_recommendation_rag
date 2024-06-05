import csv
import pandas as pd

# Path to your input CSV file
input_file_path = 'data/google_play_games1.csv'
# Path to your output CSV file
output_file_path = 'data/formatted_google_play_games.csv'

def parse_csv(file_path):
    rows = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
        headers = next(reader)  # Get the headers
        for row in reader:
            # Combine fields if the description was split due to commas within quotes
            if len(row) > 6:
                row[5] = ','.join(row[5:])
                row = row[:6]
            elif len(row) < 6:
                print(f"Skipping malformed row: {row}")
                continue
            rows.append(row)
    return headers, rows

# Read and parse the CSV file
headers, rows = parse_csv(input_file_path)

# Create DataFrame from the cleaned data
df = pd.DataFrame(rows, columns=headers)

# Function to format each row
def format_row(row):
    return {
        "Title": f'"{row["Title"]}"',
        "Link": f'"{row["Link"]}"',
        "Category": f'"{row["Category"]}"',
        "Rating": f'"{row["Rating"]}"',
        "Thumbnail": f'"{row["Thumbnail"]}"',
        "Description": f'"{row["Description"]}"'
    }

# Format each row and prepare for output
formatted_rows = [format_row(row) for index, row in df.iterrows()]

# Create a new DataFrame for the formatted rows
formatted_df = pd.DataFrame(formatted_rows)

# Save the formatted DataFrame to a new CSV file
formatted_df.to_csv(output_file_path, index=False, quoting=csv.QUOTE_ALL)

print(f"Formatted data saved to {output_file_path}")
