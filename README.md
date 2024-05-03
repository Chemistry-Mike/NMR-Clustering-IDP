# NMR-Clustering-IDP
**Description** This repository contains many of the codes and scripts necessary to generate unique conformational ensembles from molecular dynamics trajectories.

## (1) Generating Trajectory Information

Before running the scripts, make sure that the following files are contained in subdirectory, _INPUT_, below where you are running the python scripts in. Here is the formats that are required for the **generate_traj_info.py** script:

- Compressed trajectory file **($NAME.xtc)**
- Topology file **($NAME.TPR / $NAME.GRO / $NAME.PDB)**

Once the script is executed, it should generate a pickle file (**$NAME**-INFO.pkl) in the _OUTPUT_ folder containing a DICT with each of the following obtained from the trajectory:

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

Once the file **$NAME**-INFO.pkl is generated, you can then run the script **generate_traj_info.py** to generate 2D latent spaces from the input features.

The following linear DR techniques will be implemented:
- PCA: Principal Component Analysis (key = "pca")
- TICA: Time-Independent Component Analysis (key = "tica")

The following non-linear DR techniques will be implemented:
- tSNE: t-distributed Stochastic Neighbor Embedding (key = "tsne")

Once the script is executed, it should generate a pickle file (**$NAME**-DR.pkl) in the _OUTPUT_ folder containing a DICT which scans through each of the input features, and implements different perplexities.

## (3) Running Clustering Algorithm

Once the Dimensionality Reduction is complete (**$NAME**-DR.pkl), the pickle file can then be passed through the **generate_clusters_info.py** script.

The clustering will be implemented on each of the DR latent spaces for cluster sizes from the following:
- 2, 3, 4, 5, 6, 7, 8, 9, 10 ,15 ,20 ,25 ,30 ,35 ,40 ,45 ,50 ,60 ,70 ,80 ,90 ,100 ,150 ,200 ,300 ,400

The resultant file will be (**NAME**-CA.pkl) in the _OUTPUT_ folder containing the labels from each of these clustering algorithms.

## (4) Analyze Cluster Quality

Once the Clustering is complete, the Davies-Bouldin Score, Silhouette Score, and Integrated Silhouette Score can be computed to get an understanding of the quality of the clustering.

Run the script **compute_ss_db.py**.

This will scan through the clusters output in **NAME**-CA.pkl, compare them to the latent space **$NAME**-DR.pkl for the DB and SS, and compare to the original data in **$NAME**-INFO.pkl to compute the SS_Int.

A new file, **$NAME**-SS-DB.pkl, will be generated from this script.

## (5) Generate Ensembles

Once everything is complete, the actual ensembles can be generated. Run the script **generate_ensemble.py** to output the ensembles into the folder _ENSEMBLE_.

## (6) Assess Quality of Ensembles - Experimental Chemical Shifts

If there exists some chemical shift information, you should be able to quickly assess the quality of the ensembles by running a quick side script, **assess_chemical_shifts.py**.

The output for this script will be a .txt file and a .pdf file showing correlation plots, RSQ values, and RMSE values in plots, as well a pickle file **$NAME-Compare-EXP.pkl**

