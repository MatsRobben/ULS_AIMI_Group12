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
ZIP_FILE="$HOME/validation_baseline_more_training.zip"

# Create the zip file containing only .json and .nii.gz files
zip -j $ZIP_FILE ${SOURCE_DIR}*.json ${SOURCE_DIR}*.nii.gz

rm -r $SOURCE_DIR
mkdir $HOME/results
cp -r $nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_200_EighthLR__nnUNetPlansNoRs__3d_fullres_resenc/ $HOME/results
