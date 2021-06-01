# SPDS800 - Data Science Master's Thesis

__Thesis title:__ ELECTRICITY CONSUMPTION FORECAST OF RESIDENTIAL HOUSING USING DEEP NEURAL NETWORKS  
__Author:__ Nicolai Bo Vanting  
__Affiliation:__ University of Southern Denmark (SDU)  
__Semester:__ Spring/Summer, 2021
  
  
This repository contains the code for the master's thesis.  
Each notebook has its corresponding chapter from the thesis in the title.  

## Guide

In the [external](https://github.com/nbvanting/thesis/tree/main/external) folder all code for loading the external data from DMI and the day lengths can be found.  
  
The [model](https://github.com/nbvanting/thesis/tree/main/model) folder contains all code related to:
 - Data Processing, Preparation, and Exploration
 - Feature Selection & Engineering
 - Model Training
    - Benchmark, Baseline, and Proposed Model
 - All code run in Google Colab found in the [Colab](https://github.com/nbvanting/thesis/tree/main/model/Colab) folder
 - All visualizations in the [visuals](https://github.com/nbvanting/thesis/tree/main/model/visuals) folder
    - Including plots, charts, and figures
 - All trained models as .h5 files in [models](https://github.com/nbvanting/thesis/tree/main/model/models)
    - Including the training history of the final model as a pkl
 - Hyperparameter Tuning Sweeps
 - Utility, Pipeline, and Helper functions are found in the [utils](https://github.com/nbvanting/thesis/tree/main/model/utils) folder  

