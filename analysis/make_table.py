import json
import os
import numpy as np
from tqdm import tqdm
import SimpleITK as sitk
from skimage.measure import label
import pandas as pd

# Define the paths to the source directories
true_labels_source_dir = 'data_full/Dataset001_ULS/labelsTr/'
predicted_labels_source_dir = 'validation/validation_baseline_full'

# Get a list of all files in the predicted and true labels folders
predicted_labels = os.listdir(predicted_labels_source_dir)
true_labels = os.listdir(true_labels_source_dir)

# Filter the list to include only files ending with .nii.gz
predicted_nii_files = [f for f in predicted_labels if f.endswith('.nii.gz')]
true_nii_files = [f for f in true_labels if f.endswith('.nii.gz')]

# Function to compute lesion sizes and number of connected components
def compute_lesion_stats(source_dir, nii_files):
    lesion_data = {}
    for nii_file in tqdm(nii_files):
        image_file = os.path.join(source_dir, nii_file)
        image_metadata = sitk.ReadImage(image_file)
        image_data = sitk.GetArrayFromImage(image_metadata)
        
        # Compute lesion size in voxels
        lesion_size_voxels = np.sum(image_data)  # Assuming binary mask where lesion voxels are 1
        
        # Compute number of connected components
        labeled_array, num_components = label(image_data, return_num=True)
        
        # Compute voxel spacing
        spacing = image_metadata.GetSpacing()  # Returns spacing in (x, y, z) order
        voxel_volume = spacing[0] * spacing[1] * spacing[2]
        
        # Compute lesion size in mm^3
        lesion_size_mm3 = lesion_size_voxels * voxel_volume
        
        case_name = nii_file.replace('.nii.gz', '')
        lesion_data[case_name] = {
            'lesion_size_voxels': lesion_size_voxels,
            'lesion_size_mm3': lesion_size_mm3,
            'num_components': num_components
        }
    return lesion_data

# Compute lesion sizes for predicted and true segmentations
predicted_lesion_data = compute_lesion_stats(predicted_labels_source_dir, predicted_nii_files)
true_lesion_data = compute_lesion_stats(true_labels_source_dir, true_nii_files)

# Define the path to the JSON file
json_file_path = 'validation/validation_baseline_full/summary.json'

# Load the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Initialize an empty list to store the results
metrics_list = []

# Iterate over each data point in 'metric_per_case' and add lesion sizes
for data_point in data['metric_per_case']:
    # Extract the prediction file path
    prediction_file = data_point['prediction_file']
    reference_file = data_point['reference_file']
    
    # Extract the case name from the prediction file path
    case_name = os.path.basename(prediction_file).replace('.nii.gz', '')
    
    # Extract the metrics
    metrics = data_point['metrics']['1']
    
    # Add the case name to the metrics dictionary
    metrics['case_name'] = case_name
    
    # Add the predicted and true lesion sizes and number of connected components to the metrics dictionary
    metrics['true_lesion_size_voxels'] = true_lesion_data.get(case_name, {}).get('lesion_size_voxels', 0)
    metrics['true_lesion_size_mm3'] = true_lesion_data.get(case_name, {}).get('lesion_size_mm3', 0)
    metrics['true_num_components'] = true_lesion_data.get(case_name, {}).get('num_components', 0)
    metrics['predicted_lesion_size_voxels'] = predicted_lesion_data.get(case_name, {}).get('lesion_size_voxels', 0)
    metrics['predicted_lesion_size_mm3'] = predicted_lesion_data.get(case_name, {}).get('lesion_size_mm3', 0)
    metrics['predicted_num_components'] = predicted_lesion_data.get(case_name, {}).get('num_components', 0)
    metrics['lesion_size_voxels_error'] = (metrics['true_lesion_size_voxels'] - metrics['predicted_lesion_size_voxels'])
    metrics['lesion_size_mm3_error'] = (metrics['true_lesion_size_mm3'] - metrics['predicted_lesion_size_mm3'])
    metrics['num_components_error'] = (metrics['true_num_components'] - metrics['true_num_components'])
    
    # Append the metrics dictionary to the list
    metrics_list.append(metrics)

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(metrics_list)

# Display the DataFrame
print(df)

parquet_file_path = 'lesion_metrics_baseline_full.parquet'
df.to_parquet(parquet_file_path, index=False)
