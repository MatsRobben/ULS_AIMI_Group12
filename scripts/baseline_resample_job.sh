#!/bin/sh

#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --gpus=1
#SBATCH --mem=32G
#SBATCH --time=40:00:00
#SBATCH --gpus-per-node=1

# Go to temp folder
cd $TMPDIR

# Load moduels
module load 2022
module load Python/3.10.4-GCCcore-11.3.0
python3 -m pip install --user --upgrade pip

# Clone nnUNet and install all requirements
git clone --no-checkout https://github.com/MIC-DKFZ/nnUNet.git
cd nnUNet
git checkout 947eafbb9adb5eb06b9171330b4688e006e6f301
pip3 install -e .

mkdir data data/nnUNet_raw data/nnUNet_results data/nnUNet_preprocessed

# Create env variables
export nnUNet_raw="$TMPDIR/nnUNet/data/nnUNet_raw"
export nnUNet_results="$TMPDIR/nnUNet/data/nnUNet_results"
export nnUNet_preprocessed="$TMPDIR/nnUNet/data/nnUNet_preprocessed"

# Change these lines to flush the STDOUT, otherwhise it does not update the output file during training.
sed -i '463s/.*/                print(*args, flush=True)/' nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py
sed -i '465s/.*/            print(*args, flush=True)/' nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py

# copy extentions
cp -r $HOME/ULS_AIMI_Group12/extensions/nnunetv2/ .

# Copy model
cp $HOME/zip_folder/Dataset001_ULS.zip $nnUNet_results
unzip $nnUNet_results/Dataset001_ULS.zip -d $nnUNet_results
rm $nnUNet_results/Dataset001_ULS.zip
#cp $nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_500_QuarterLR__nnUNetPlansNoRs__3d_fullres_resenc/fold_all/checkpoint_best.pth \
#$nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_500_QuarterLR__nnUNetPlansNoRs__3d_fullres_resenc/fold_all/checkpoint_final.pth

# Copy plans file
mkdir $nnUNet_preprocessed/Dataset001_ULS
cp $nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_500_QuarterLR__nnUNetPlansNoRs__3d_fullres_resenc/plans.json \
$nnUNet_preprocessed/Dataset001_ULS/nnUNetPlansNoRs.json

# Copy data
cp -r $HOME/data_full/Dataset001_ULS/ $nnUNet_raw/Dataset001_ULS

#############################################################
# Resample worst performing files
#############################################################
# Define the directories
images_dir="$nnUNet_raw/Dataset001_ULS/imagesTr"
labels_dir="$nnUNet_raw/Dataset001_ULS/labelsTr"

# Path to the JSON file containing lesion names to resample
json_file="$HOME/ULS_AIMI_Group12/analysis/resample_list.json"

# Read the JSON file and parse the lesion names into an array
lesion_names=$(jq -r '.[]' "$json_file")

# Specify the number of times to resample each lesion
num_resamples=1  # Change this to the desired number of resamples

# Initialize a counter for resampling
counter=0

# Loop through each lesion name
for lesion_name in $lesion_names; do
    # Loop for the specified number of resamples
    for ((i=0; i<num_resamples; i++)); do
        # Define the zero-padded counter
        padded_counter=$(printf "%03d" $counter)

        # Define the source and destination file paths for images and labels
        image_src="${images_dir}/${lesion_name}_0000.nii.gz"
        label_src="${labels_dir}/${lesion_name}.nii.gz"
        
        image_dst="${images_dir}/resample_${padded_counter}_0000.nii.gz"
        label_dst="${labels_dir}/resample_${padded_counter}.nii.gz"

        # Check if the source files exist
        if [[ -f "$image_src" && -f "$label_src" ]]; then
            # Copy and rename the files
            cp "$image_src" "$image_dst"
            cp "$label_src" "$label_dst"
            echo "Resampled $lesion_name to resample_${padded_counter}"
        else
            echo "Warning: Source files for $lesion_name not found!"
        fi

        # Increment the counter
        counter=$((counter + 1))
    done
done

# Change dataset.json file
dataset_file="$nnUNet_raw/Dataset001_ULS/dataset.json"
current_num_training=$(grep -oP '"numTraining":\s*\K\d+' "$dataset_file")
new_num_training=$((current_num_training + counter))
sed -i.bak -E "s/(\"numTraining\":\s*)[0-9]+/\1$new_num_training/" "$dataset_file"
#############################################################
# End resmpale
#############################################################

# Process the data and make a plans
nnUNetv2_extract_fingerprint -d 1
nnUNetv2_plan_experiment -d 1
nnUNetv2_preprocess -d 1 -p nnUNetPlansNoRs

# Train model
export pretrained="$nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_500_QuarterLR__nnUNetPlansNoRs__3d_fullres_resenc/fold_all/checkpoint_best.pth"
nnUNetv2_train 1 3d_fullres_resenc all -p nnUNetPlansNoRs -tr nnUNetTrainer_ULS_200_EighthLR -pretrained_weights $pretrained --npz

# copy results
# Define the source directory and the output zip file name
SOURCE_DIR="$nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_200_EighthLR__nnUNetPlansNoRs__3d_fullres_resenc/fold_all/validation/"
ZIP_FILE="$HOME/validation_baseline_resample.zip"

# Create the zip file containing only .json and .nii.gz files
zip -j $ZIP_FILE ${SOURCE_DIR}*.json ${SOURCE_DIR}*.nii.gz

rm -r $SOURCE_DIR
mkdir $HOME/results
cp -r $nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_200_EighthLR__nnUNetPlansNoRs__3d_fullres_resenc/ $HOME/results
