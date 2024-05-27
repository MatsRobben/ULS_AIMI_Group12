import os
import json
import shutil

# Define the number of lowest scoring entries to select
num_lowest_entries = 100
destination_folder = 'worst_cases'

# Define the paths to the source directories
images_source_dir = 'data/Dataset001_ULS/imagesTr/'
true_labels_source_dir = 'data/Dataset001_ULS/labelsTr/'
predicted_labels_source_dir = 'validation/'

# Clear the destination folder if it exists, or create it if it doesn't
if os.path.exists(destination_folder):
    shutil.rmtree(destination_folder)
os.makedirs(destination_folder)
os.makedirs(os.path.join(destination_folder, 'images'))
os.makedirs(os.path.join(destination_folder, 'true_labels'))
os.makedirs(os.path.join(destination_folder, 'predicted_labels'))

# Define the path to the JSON file
json_file_path = 'validation/summary.json'

# Load the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)


# Initialize an empty dictionary to store the results
case_dice_scores = {}

# Iterate over each data point in 'metric_per_case'
for data_point in data['metric_per_case']:
    # Extract the prediction file path
    prediction_file = data_point['prediction_file']
    
    # Extract the case name from the prediction file path
    case_name = os.path.basename(prediction_file).replace('.nii.gz', '')
    
    # Extract the Dice score
    dice_score = data_point['metrics']['1']['Dice']
    
    # Add the case name and Dice score to the dictionary
    case_dice_scores[case_name] = dice_score

# Print the case names with Dice score equal to zero
zero_dice_cases = [case for case, score in case_dice_scores.items() if score == 0]
print(f"There are a {len(zero_dice_cases)} cases with Dice score equal to zero:")

# Sort the dictionary by Dice scores and get the specified number of lowest scoring entries
lowest_entries = sorted(case_dice_scores.items(), key=lambda x: x[1])[:num_lowest_entries]

# Print the lowest scoring entries with their names and Dice scores
print(f"Lowest {num_lowest_entries} scoring entries:")
for case, score in lowest_entries:
    print(f"Case: {case}, Dice Score: {score}")


# Copy worst cases to the destination folder
for case, _ in lowest_entries:
    # Copy images
    shutil.copy2(os.path.join(images_source_dir, f'{case}_0000.nii.gz'), os.path.join(destination_folder, 'images'))
    # Copy true labels
    shutil.copy2(os.path.join(true_labels_source_dir, f'{case}.nii.gz'), os.path.join(destination_folder, 'true_labels'))
    # Copy predicted labels
    shutil.copy2(os.path.join(predicted_labels_source_dir, f'{case}.nii.gz'), os.path.join(destination_folder, 'predicted_labels'))

print(f"{num_lowest_entries} worst cases copied to '{destination_folder}'.")