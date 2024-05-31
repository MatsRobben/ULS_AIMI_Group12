import json
import os
import numpy as np
import shutil
from tqdm import tqdm
import SimpleITK as sitk
import pandas as pd

from figures import plot_histograms, plot_scatterplots, plot_histograms_two_groups

# Define the paths to the source directories
images_source_dir = 'data/Dataset001_ULS/imagesTr/'
true_labels_source_dir = 'data/Dataset001_ULS/labelsTr/'
predicted_labels_source_dir = 'validation/'

# Define the path to the Parquet file
parquet_file_path = 'lesion_metrics_baseline.parquet'

# Load the Parquet file into a pandas DataFrame
df = pd.read_parquet(parquet_file_path)

# Display the DataFrame
print(df.columns)
print(df)

# df = df[df['Dice'] == 0]
# print(df)

columns_to_plot = [col for col in df.columns if col != 'case_name']

# Define the directory to save the images
save_directory = 'images/baseline'

plot_histograms(df, columns_to_plot, save_directory)
plot_scatterplots(df, [('Dice', 'lesion_size_voxels_error')], save_directory)
plot_scatterplots(df, [('Dice', 'lesion_size_voxels_error')], save_directory)
plot_scatterplots(df, [('Dice', 'true_lesion_size_voxels'), ('Dice', 'predicted_lesion_size_voxels')], save_directory)
plot_histograms_two_groups(df, ['true_lesion_size_voxels', 'predicted_lesion_size_voxels', 'predicted_num_components'], save_directory)
plot_scatterplots(df, [('predicted_lesion_size_voxels', 'true_lesion_size_voxels')], save_directory)
plot_scatterplots(df, [('true_lesion_size_voxels', 'predicted_num_components'), ('predicted_lesion_size_voxels', 'predicted_num_components')], save_directory)

# Define the directory to save the images
save_directory = 'images/baseline/zero_group'

df = df[df['Dice'] == 0]

plot_histograms(df, columns_to_plot, save_directory)
plot_scatterplots(df, [('predicted_lesion_size_voxels', 'true_lesion_size_voxels')], save_directory)
plot_scatterplots(df, [('true_lesion_size_voxels', 'predicted_num_components'), ('predicted_lesion_size_voxels', 'predicted_num_components')], save_directory)