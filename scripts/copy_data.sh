#!/bin/bash

# Navigate to the root of the file system
cd /

# Define the output directory for the merged dataset
output_dir="$HOME/data_full/Dataset001_ULS"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Define the paths to the datasets
datasets=(
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset500_DeepLesion3D"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset501_RadboudumcBone"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset502_RadboudumcPancreas"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset503_kits21"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset504_LIDC-IDRI"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset505_LiTS"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset506_MDSC_Task06_Lung"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset507_MDSC_Task07_Pancreas"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset508_MDSC_Task10_Colon"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset509_NIH_LN_ABD"
    "/projects/0/nwo2021061/uls23/nnUNet_raw/Dataset510_NIH_LN_MED"
)

# Function to check for filename overlaps
check_filename_overlap() {
    local folder="$1"
    declare -A filenames

    for dataset in "${datasets[@]}"; do
        for file in "$dataset/$folder"/*; do
            base_file=$(basename "$file")
            if [[ -n ${filenames["$base_file"]} ]]; then
                echo "Error: Filename overlap detected between ${filenames["$base_file"]} and $dataset in $folder"
                exit 1
            else
                filenames["$base_file"]=$dataset
            fi
        done
    done
}

# Check for filename overlaps in imagesTr, imagesTs, and labelsTr folders
#for folder in imagesTr imagesTs labelsTr; do
#    check_filename_overlap "$folder"
#done

# Merge the imagesTr, imagesTs, and labelsTr folders with progress
for folder in imagesTr imagesTs labelsTr; do
    mkdir -p "$output_dir/$folder"
    for dataset in "${datasets[@]}"; do
        rsync -r --info=progress2 "$dataset/$folder"/ "$output_dir/$folder"/
    done
done

# Create the dataset.json file
num_training_samples=$(find "$output_dir/labelsTr" -type f | wc -l)
cat <<EOF > "$output_dir/dataset.json"
{
 "channel_names": {
   "0": "dummy_channel"
 },
 "labels": {
   "background": 0,
   "foreground": 1
 },
 "numTraining": $num_training_samples,
 "file_ending": ".nii.gz",
 "overwrite_image_reader_writer": "SimpleITKIO"
}
EOF

echo "Merging datasets completed successfully!"

