#!/bin/sh

#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --gpus=1
#SBATCH --mem=40G
#SBATCH --time=120:00:00
#SBATCH --gpus-per-node=1

# Go to temp folder
cd $TMPDIR

# Load moduels
module load 2022
module load Python/3.10.4-GCCcore-11.3.0
python3 -m pip install --user --upgrade pip

# Clone nnUNet and install all requirements
git clone https://github.com/MIC-DKFZ/nnUNet.git
cd nnUNet
pip install -e .

# Change these lines to flush the STDOUT, otherwhise it does not update the output file during training.
sed -i '471s/.*/                print(*args, flush=True)/' nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py
sed -i '473s/.*/            print(*args, flush=True)/' nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py

# Create folders
mkdir nnUNet_raw nnUNet_results nnUNet_preprocessed

# Create env variables
export nnUNet_raw="$TMPDIR/nnUNet/nnUNet_raw"
export nnUNet_results="$TMPDIR/nnUNet/nnUNet_results"
export nnUNet_preprocessed="$TMPDIR/nnUNet/nnUNet_preprocessed"

# Copy data
cp -r $HOME/data/Dataset001_ULS $TMPDIR/nnUNet/nnUNet_raw/Dataset001_ULS

# Process the data and make a plans
nnUNetv2_plan_and_preprocess -d 1 --verify_dataset_integrity

# Train model
for FOLD in 0 1 2 3 4; do
   nnUNetv2_train 1 3d_fullres $FOLD --npz
done

# copy results
cp -r $TMPDIR/nnUNet/nnUNet_results $HOME/results
cp -r $TMPDIR/nnUNet_preprocessed $HOME/preprocessed
