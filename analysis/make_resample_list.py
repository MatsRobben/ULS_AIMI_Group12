import pandas as pd
import json

# Define the path to the Parquet file
parquet_file_path = 'lesion_metrics_baseline.parquet'

# Load the Parquet file into a pandas DataFrame
df = pd.read_parquet(parquet_file_path)

# Define the number of lowest scoring entries to select
N = 100  # Change this number to the desired number of lowest scoring case_names

# Select the N lowest scoring case_names based on the 'Dice' column
lowest_scoring_cases = df.nsmallest(N, 'Dice')['case_name'].tolist()

# Define the path for the output JSON file
output_json_path = 'resample_list.json'

# Save the selected case names to a JSON file
with open(output_json_path, 'w') as json_file:
    json.dump(lowest_scoring_cases, json_file, indent=4)

print(f"Saved the {N} lowest scoring case names to {output_json_path}")