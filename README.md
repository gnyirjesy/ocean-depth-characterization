# ocean-depth-characterization
Data Science Capstone Project focused on extending satellite observations to ocean depths with machine learning

## Collaborators

**Mentor**: Nicholas Bock

**Instructor**: Vivian Zhang

**Team**:
- Erin Josephine Donnelly | ejd2170
- Elijan Flomen | ef2681 **(team captain)**
- Blake David Hartung | bdh2141
- Yo Xing Jeremijenko-Conley | yxj2000
- Gabrielle Nyrjesy | gn2327

**CA**: Katie Jooyoung Kim

## Project objective

Employ machine learning methods to oceanographic data obtained by satellites and BGC-Argo floats to characterize and infer subsurface phytoplankton dynamics and carbon export at a global scale. Link the high spatial and temporal resolution satellite data with the very low spatial resolution subsurface data obtained by floats. Extrapolate biomes from a previous study (Bock et al. 2020) based on satellite data.


## Results
After substantial data pre-processing, model selection, and post-processing, we ultimately landed on a multi-step procedure to predict chlorophyll a at 25 depths based solely on the location, time of year, and satellite-derived surface-level ocean measurements. At a high level, our overall approach can be summarized with the following process:

1. **Depth-normalization**: identifies the maximum euphotic zone depth and standardizes inputs for each training example respectively.
2. **XGBoost Regressor**: predicts chlorophyll a at 11 standardized depths, equally spaced with respect to the euphotic zone.
3. **Neural network**: further refines the XGB model’s predictions and combats overfitting.
4. **Post-processing**: combines predictions from the neural network with a location-specific characteristic distribution equation based on location, smooths predictions, and extends the dimensionality of the final predictions from 11 to 25. 

Our model achieves a test $R^2$ value of 0.64, demonstrating that satellite-derived surface-level ocean measurements can be used to generate subsurface chlorophyll distributions. As a result, our model acts as a potential zero-cost substitute for the otherwise resource-intensive process of manually collecting chlorophyll measurements. 

## Folder Structure

The codebase is structured as follows:

```
├── EDA: Initial EDA and visualizations of the data
├── README.md
├── model_files: trained models
├── model_inference: script to run model inference
├── model_training: script to train the model
├── normalization_and_clustering: notebooks for data pre-processing
├── preliminary_models: model drafts and exploration
├── reference_summaries: literature review
├── utils: useful functions for data querying and pre-processing
├── visualizations: saved plots
└── web_application: product UI code
```

## Product
https://ocean-app-21dd87.netlify.app/
