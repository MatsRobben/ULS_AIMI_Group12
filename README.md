# ULS_AIMI_Group12

This repository was created for the Artificial Intelligence in Medical Imaging (NWI-IMC037) project. The project is part of the Universal Lesion Segmentation (ULS) competition, which was organized by The Diagnostic Image
Analysis Group at Radboud University. The goal of the ULS competition was to create a segmentation model with improved performance and generalizability over all types of lesions in the Thorax-Abdomen area. The code in this repository accompanies the project report [Universal Lesion Segmentation: Identification of difficult cases](https://github.com/MatsRobben/ULS_AIMI_Group12/blob/main/ULS_identification_of_difficult_cases.pdf). The research focuses on the cases where the baseline model performed the worst. For the baseline model, the [nn-UNet](https://github.com/MIC-DKFZ/nnUNet) framework was used. 

The analysis can be split into two sections, the objective analysis and subjective analysis. The objective analysis was performed on all of the model's results, which are available in the [analysis](https://github.com/MatsRobben/ULS_AIMI_Group12/tree/main/analysis) folder. The subjective analysis involved manually inspecting the 100 lowest scoring lesions, which were selected due to them all having a Dice score of 0. The results of the subjective analysis can be found in [Inspection worst cases.pdf](https://github.com/MatsRobben/ULS_AIMI_Group12/blob/main/Inspection%20worst%20cases.pdf). Apart from these analyses done on the results of the baseline model, we also participated in a reader study to get a better understanding of lesion segmentation in practice. The results of this can be found in [reader study results](https://github.com/MatsRobben/ULS_AIMI_Group12/tree/main/reader%20study%20results).

Finally, the code that was used to run our experiments with the nn-UNet framework can be found in the [scripts](https://github.com/MatsRobben/ULS_AIMI_Group12/tree/main/scripts) folder. 

## Analysis

The analysis folder contains the objective analysis of the baseline results. The [make_table.py](https://github.com/MatsRobben/ULS_AIMI_Group12/blob/main/analysis/make_table.py) code takes the validation results and produces a table that contains all important attributes, such as scores, lesion size, number of components, ect. These tables can be loaded by the [analysis.py](https://github.com/MatsRobben/ULS_AIMI_Group12/blob/main/analysis/analysis.py) code, which uses [figures.py](https://github.com/MatsRobben/ULS_AIMI_Group12/blob/main/analysis/figures.py) to generate all of the figures required for the analysis and stores them in the /images folder. Two additional code files are provided, [worst_cases.py](https://github.com/MatsRobben/ULS_AIMI_Group12/blob/main/analysis/worst_cases.py) and [make_resample_list.py](https://github.com/MatsRobben/ULS_AIMI_Group12/blob/main/analysis/make_resample_list.py). The first selects and stores the worst cases to be used in the subjective analysis, and the second makes a list of worst cases that can be used during the fine-tuning on the baseline model. 

### Directory Structure

The analysis file does not contain the results of the analysis, wish should be added to run the [make_table.py](https://github.com/MatsRobben/ULS_AIMI_Group12/blob/main/analysis/make_table.py) script. If you which to run the code the folder structure should look the following:

```
analysis/
├── data/
│ └── Dataset001_ULS/
│ ├── imagesTr/
│ │ └── [training_images]
│ ├── imagesTs/
│ │ └── [test_images]
│ └── labelsTr/
│   └── [training_labels]
└── validation/
  └── [validation_files]
  └── summery.json
```

## Scripts

The [scripts](https://github.com/MatsRobben/ULS_AIMI_Group12/tree/main/scripts) folder contains all of the scripts that were used to run the nn-UNet framework. These bash files were specifically designed to work with our setup and will most likely need to be modified for other applications. The following list gives an overview of the different bash files and what they were used for.
- copy_data.sh: This file was used to merge the different datasets. The code can check for overlapping case names and update the dataset.json file.
- baseline_uls_job.sh: Is used to train a new nn-UNet model from scratch. In our case the model was only trained on a subset of the data.
- baseline_crossval.sh: Is used to train the model with 5 fold cross-validation. This was not used in the final analysis due to the associated computational cost.
- baseline_uls_val_job.sh: This code is used to load the trained baseline model and run validation on the dataset.
- baseline_resample_job.sh: This code is used to continue training the baseline, where we sample the difficult cases multiple times.

## Extensions

This folder contains extensions to the nnunetv2 framework. The baseline code already provided most of the code, however, we extended it with the class ```nnUNetTrainer_ULS_200_EighthLR```.
