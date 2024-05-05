### Import necessary packages
import mdtraj as md
import numpy as np
import pickle
import sys

### Specify the HOME directory
HOME="path/to/dir"

### Specify the location of the trajectory files (input)
xtc=HOME+"Trajectories/"+protein+"-small.xtc"
pdb=HOME+"Trajectories/"+protein+"-first.pdb"

### Specify the location of the pickle file (output)
pkl=HOME+"Pickles/Features/"+protein+"-INFO.pkl"

### Specify the sampling interval
dt = 1

### Load the trajectory
traj=md.load(xtc,top=pdb)[::dt]





