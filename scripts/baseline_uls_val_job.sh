#!/bin/sh

#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --gpus=1
#SBATCH --mem=12G
#SBATCH --time=02:00:00
#SBATCH --gpus-per-node=1

# Go to temp folder
cd $TMPDIR

# Load moduels
module load 2022
module load Python/3.10.4-GCCcore-11.3.0
python3 -m pip install --user --upgrade pip

# Clone nnUNet and install all requirements
cp -r $HOME/uls_baseline/nnUNet .
cd nnUNet
pip3 install -e .

# Change these lines to flush the STDOUT, otherwhise it does not update the output file during training.
sed -i '463s/.*/                print(*args, flush=True)/' nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py
sed -i '465s/.*/            print(*args, flush=True)/' nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py

# Create env variables
export nnUNet_raw="$TMPDIR/nnUNet/data/nnUNet_raw"
export nnUNet_results="$TMPDIR/nnUNet/data/nnUNet_results"
export nnUNet_preprocessed="$TMPDIR/nnUNet/data/nnUNet_preprocessed"

# Process the data and make a plans
nnUNetv2_extract_fingerprint -d 1
nnUNetv2_plan_experiment -d 1
nnUNetv2_preprocess -d 1 -p nnUNetPlansNoRs

# Train model
export pretrained="$nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_500_QuarterLR__nnUNetPlansNoRs__3d_fullres_resenc/fold_all/checkpoint_best.pth"
nnUNetv2_train 1 3d_fullres_resenc all -p nnUNetPlansNoRs -tr nnUNetTrainer_ULS_500_QuarterLR -pretrained_weights $pretrained --val --val_best --npz

# copy results
cp -r $nnUNet_results/Dataset001_ULS/nnUNetTrainer_ULS_500_QuarterLR__nnUNetPlansNoRs__3d_fullres_resenc/fold_all/validation $HOME/results