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
parquet_file_path = 'lesion_metrics.parquet'

# Load the Parquet file into a pandas DataFrame
df = pd.read_parquet(parquet_file_path)

# Display the DataFrame
print(df.columns)
print(df)

columns_to_plot = [col for col in df.columns if col != 'case_name']

# Define the directory to save the images
save_directory = 'images'

plot_scatterplots(df, [('predicted_lesion_size', 'true_lesion_size')], save_directory)
# plot_histograms(df, columns_to_plot, save_directory)

# plot_histograms_two_groups(df, ['true_lesion_size', 'true_num_components',
#                                 'predicted_lesion_size', 'predicted_num_components',
#                                 'lesion_size_error', 'num_components_error'], save_directory)