# NMR-Clustering-IDP
**Description** This repository contains many codes and scripts to generate unique conformational ensembles from molecular dynamics trajectories.

## (1) Generating Trajectory Information

Before running the scripts, ensure the following files are contained in the subdirectory, _Trajectories_, below where you run the Python scripts. Here are the formats that are required for the **generate_traj_info.py** script:

- Compressed trajectory file **(TEST.xtc)**
- Topology file **(TEST.TPR / TEST.GRO / TEST.PDB)**

Once the script is executed, it should generate a pickle file (**TEST**-INFO.pkl) in the _Features_ folder containing a DICT with each of the following obtained from the trajectory:

- RMSD (key = "rmsd")
- Radius of Gyration (key = "rg")
- End-to-End Distance (key = "e2e")
- Solvent-Accessible Surface Area (key = "sasa")
- RMSF (key = "rmsf")
- Alpha Carbon Distances (key = "dist")
- Alpha Carbon Angles (key = "ang")
- Phi Dihedral Angle (key = "phi")
- Psi Dihedral Angle (key = "psi")

## (2) Running Dimensionality Reduction

Once the file **TEST**-INFO.pkl is generated, you can run the script **generate_dim_red.py** to generate 2D latent spaces from the input features.

The following linear DR techniques will be implemented:
- PCA: Principal Component Analysis (key = "pca")
- TICA: Time-Independent Component Analysis (key = "tica")

The following non-linear DR techniques will be implemented:
- tSNE: t-distributed Stochastic Neighbor Embedding (key = "tsne")

Once the script is executed, it should generate a pickle file (**TEST**-DR.pkl) in the _DimRed_ folder containing a DICT, which scans through each input feature and implements different perplexities.

## (3) Running Clustering Algorithm

Once the Dimensionality Reduction is complete (**TEST**-DR.pkl), the pickle file can be passed through the **generate_clusters_labels.py** script.

The clustering will be implemented on each of the DR latent spaces for cluster sizes from the following:
- 2, 3, 4, 5, 6, 7, 8, 9, 10 ,15 ,20 ,25 ,30 ,35 ,40 ,45 ,50 ,60 ,70 ,80 ,90 ,100 ,150 ,200 ,300 ,400

The resultant file will be (**TEST**-CA.pkl) in the _Clustering_ folder containing the labels from each clustering algorithm.

## (4) Analyze Cluster Quality

Once the Clustering is complete, the Davies-Bouldin Score, Silhouette Score, and Integrated Silhouette Score can be computed to understand the clustering quality.

Run the script **compute_ss_db.py**.

This will scan through the clusters output in **TEST**-CA.pkl, compare them to the latent space **TEST**-DR.pkl for the DB and SS, and compare to the original data in **TEST**-INFO.pkl to compute the SS_Int.

A new file, **TEST**-SS-DB.pkl, will be generated from this script.

## (5) Generate Ensembles

Once everything is complete, the actual ensembles can be generated. Run the script **generate_ensemble.py** to output the ensembles into the folder _ENSEMBLE_.

## (6) Assess Quality of Ensembles - Experimental Chemical Shifts

If some chemical shift information exists, you should be able to quickly assess the quality of the ensembles by running a quick side script, **assess_chemical_shifts.py**.

The output for this script will be a .txt file and a .pdf file showing correlation plots, RSQ values, and RMSE values in plots, as well as a pickle file **TEST-Compare-EXP.pkl**

