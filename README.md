# NMR-Clustering-IDP
**Description** This repository contains many of the codes and scripts necessary to generate unique conformational ensembles from molecular dynamics trajectories.

** (1) Generating Trajectory Information **

Before running the scripts, make sure that the following files are contained in the folder you are running the python scripts in. Here is the formats that are required for the "generate_traj_info.py" script:

[ ] - Compressed trajectory file **(XTC)**
[ ] - Topology file **(TPR / GRO / PDB)**

Once the script is executed, it should generate a pickle file (**NAME**-INFO.pkl) containing a DICT with each of the following obtained from the trajectory:

[ ] - RMSD (key = "rmsd")
[ ] - Radius of Gyration (key = "rg")
[ ] - End-to-End Distance (key = "e2e")
[ ] - Solvent-Accessible Surface Area (key = "sasa")
[ ] - RMSF (key = "rmsf")
