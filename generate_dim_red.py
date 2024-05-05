### Import necessary packages
import numpy as np
from sklearn.manifold import TSNE
from deeptime.decomposition import TICA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle
import sys
import math
import mdtraj as md

### Specify the HOME directory 
HOME="path/to/dir"

### Specifies the name of the system being investigated
protein="TEST"

### Specify the location of the features pickle (input)
INFO = pickle.load(open(HOME+"6-Conda/1-PICKLES/INFO/"+protein+"-INFO.pkl","rb"))
### Specify the location of the pickle file (output) 
PKL = HOME+"6-Conda/1-PICKLES/DR/"+protein+"-DimRed.pkl"

### Generate a DataFrame of the alpha carbons from the trajectory
PDB = HOME+"0-Trajectories/"+protein+"-first.pdb"
traj=md.load(PDB,top=PDB)
atoms, bonds = traj.topology.to_dataframe()

### Generate lists of all the oxygen, hydrogen, and nitrogen atoms
o_atoms = atoms[atoms.element=="O"].index
h_atoms = atoms[atoms.element=="H"].index
n_atoms	= atoms[atoms.element=="N"].index
ho_atoms = atoms[(atoms.element=="O")|(atoms.element=="H")].index

### Creates a function to do a linear PCA dimensionality reduction on the input features
def runPCA(data,ndim=2):
    pca = PCA(n_components=ndim).fit_transform(data)
    pca_data=pca[:, :2].T
    return pca_data

### Creates a function to do a linear tICA dimensionality reduction on the input features
def runTICA(features, dimensions=2, lag=20):
    estimator = TICA(dim=dimensions, lagtime=lag).fit(features)
    tica_data = estimator.fetch_model().transform(features[::dt]).T
    return tica_data

### Creates a function to do a nonlinear tICA dimensionality reduction on the input features
def runtSNE(data,perp=40,dim=2):
    print("Running tSNE...")
    tsne = TSNE(n_components=dim, random_state=42, perplexity=perp)
    tsne_data = tsne.fit_transform(data[::dt])
    return tsne_data

### Introduces a standard scalar to each of the input features
scaler = StandardScaler()
phipsi=scaler.fit_transform(np.hstack([INFO["phi"],INFO["psi"]]))
distang=scaler.fit_transform(np.hstack([INFO["dist"],INFO["ang"]]))
sasa=scaler.fit_transform(INFO["sasa"])
sasa_o=scaler.fit_transform(INFO["sasa"].T[o_atoms].T)
sasa_ho=scaler.fit_transform(INFO["sasa"].T[ho_atoms].T)
sasa_h=scaler.fit_transform(INFO["sasa"].T[h_atoms].T)
sasa_n=scaler.fit_transform(INFO["sasa"].T[n_atoms].T)
all=scaler.fit_transform(np.hstack([phipsi,distang,sasa]))
all_o=scaler.fit_transform(np.hstack([phipsi,distang,sasa_o]))
all_ho=scaler.fit_transform(np.hstack([phipsi,distang,sasa_ho]))

### Generates the tICA latent spaces
info={}
info["tica"]={}
info["tica"]["phipsi"]=runTICA(phipsi)
info["tica"]["distang"]=runTICA(distang)
info["tica"]["sasa"]=runTICA(sasa)
info["tica"]["sasa_o"]=runTICA(sasa_o)
info["tica"]["sasa_h"]=runTICA(sasa_h)
info["tica"]["sasa_ho"]=runTICA(sasa_ho)
info["tica"]["sasa_n"]=runTICA(sasa_n)
info["tica"]["all"]=runTICA(all)
info["tica"]["all_o"]=runTICA(all_o)
info["tica"]["all_ho"]=runTICA(all_ho)

### Generates the PCA latent spaces
info["pca"]={}
info["pca"]["phipsi"]=runPCA(phipsi)
info["pca"]["distang"]=runPCA(distang)
info["pca"]["sasa"]=runPCA(sasa)
info["pca"]["sasa_o"]=runPCA(sasa_o)
info["pca"]["sasa_h"]=runPCA(sasa_h)
info["pca"]["sasa_ho"]=runPCA(sasa_ho)
info["pca"]["sasa_n"]=runPCA(sasa_n)
info["pca"]["all"]=runPCA(all)
info["pca"]["all_o"]=runPCA(all_o)
info["pca"]["all_ho"]=runPCA(all_ho)

### Generate the tSNE latent spaces while scanning through a list of perplexities. This may need to be adjusted after observing the resultant DRs.
info["tsne"]={}
for perp in [10,20,30,40,50,60,70,80,90,100,150,200]:
    info["tsne"][perp]={}
    info["tsne"][perp]["phipsi"]=runtSNE(phipsi,perp)
    info["tsne"][perp]["distang"]=runtSNE(distang,perp)
    info["tsne"][perp]["sasa"]=runtSNE(sasa,perp)
    info["tsne"][perp]["sasa_o"]=runtSNE(sasa_o,perp)
    info["tsne"][perp]["sasa_ho"]=runtSNE(sasa_ho,perp)
    info["tsne"][perp]["sasa_h"]=runtSNE(sasa_h,perp)
    info["tsne"][perp]["sasa_n"]=runtSNE(sasa_n,perp)
    info["tsne"][perp]["all"]=runtSNE(all,perp)
    info["tsne"][perp]["all_o"]=runtSNE(all_o,perp)
    info["tsne"][perp]["all_ho"]=runtSNE(all_ho,perp)

### Dump the DICT into a pickle file for later analysis.
pickle.dump(info,open(PKL,'wb'))
