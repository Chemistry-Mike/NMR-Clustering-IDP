### Import necessary packages
import mdtraj as md
import numpy as np
import pickle
import sys

### Specify the HOME directory
HOME="path/to/dir"

### Specify the system being investigated
protein="TEST"

### Specify the location of the trajectory files (input)
xtc=HOME+"Trajectories/"+protein+"-small.xtc"
pdb=HOME+"Trajectories/"+protein+"-first.pdb"

### Specify the location of the pickle file (output)
pkl=HOME+"Pickles/Features/"+protein+"-INFO.pkl"

### Specify the sampling interval
dt = 1

### Load the trajectory
traj=md.load(xtc,top=pdb)[::dt]

### Load the features from the trajectory into a DICT file - info
info={}
info["phi"]=md.compute_phi(traj, periodic=True, opt=True)[1]
info["psi"]=md.compute_psi(traj, periodic=True, opt=True)[1]
info["rmsd"]=md.rmsd(traj,traj[0])
info["rg"]=md.compute_rg(traj)
info["sasa"]=md.shrake_rupley(traj)
info["rmsf"]=md.rmsf(traj,traj,0)

### Generate a DataFrame of the alpha carbons from the trajectory
atoms=traj.topology.to_dataframe()[0]
info["atoms"]=atoms
traj_Ca_atoms = atoms[atoms.name == "CA"]

### Generate the alpha carbon distances and angles
atom_pairs=[]
for n in range(len(traj_Ca_atoms.serial)-1):
    atom_pairs.append([np.array(traj_Ca_atoms.serial)[n],np.array(traj_Ca_atoms.serial)[n+1]])
info["dist"]=md.compute_distances(traj,atom_pairs)

atom_trios=[]
for n in range(len(traj_Ca_atoms.serial)-2):
    atom_trios.append([np.array(traj_Ca_atoms.serial)[n],np.array(traj_Ca_atoms.serial)[n+1],np.array(traj_Ca_atoms.serial)[n+2]])
info["ang"] = md.compute_angles(traj,atom_trios)

### Compute the end-to-end distances from the trajectory
first,last = list(traj_Ca_atoms.serial)[0],list(traj_Ca_atoms.serial)[-1]
info["e2e"] = md.compute_distances(traj,[[first,last]])

### Output the DICT into a pickle file, and save it.
pickle.dump(info, open(pkl, 'wb'))
