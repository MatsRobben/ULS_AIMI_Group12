#!/bin/bash

# Define the source directory and the output zip file name
SOURCE_DIR="results/nnUNet_results/Dataset001_ULS/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_fullres/fold_all/validation/"
ZIP_FILE="validation.zip"

# Create the zip file containing only .json and .nii.gz files
zip -j $ZIP_FILE ${SOURCE_DIR}*.json ${SOURCE_DIR}*.nii.gz

echo "Zip file $ZIP_FILE created successfully."
