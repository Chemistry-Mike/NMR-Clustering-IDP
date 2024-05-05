#!/bin/bash

ml GROMACS/2023.1-foss-2022a

protein="Bp53"

XTC=/mnt/proj1/open-27-2/bakkerm/0-Trajectories/$protein"-small.xtc"
PDB=/mnt/proj1/open-27-2/bakkerm/0-Trajectories/$protein"-first.pdb"
DAT=/mnt/proj1/open-27-2/bakkerm/6-Conda/1-PICKLES/DSSP/$protein"-DSSP.dat"

gmx dssp -f $XTC -s $PDB -hmode dssp -o $DAT
