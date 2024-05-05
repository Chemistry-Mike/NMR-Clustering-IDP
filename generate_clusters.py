### Import necessary packages 
import pickle
import numpy as np
import sys
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics

### Specify the HOME directory  
HOME="path/to/dir"

### Specifies the name of the system being investigated
protein="TEST"

### Specify the location of the dimensionality reduction pickle (input)
inp = HOME+"/DimRed/"+protein+"-DimRed.pkl"
### Specify the location of the pickle file (output) 
pkl = HOME+"/Clusters/"+protein+"-cluster.pickle"

### Loads the dimensionality reduction pickle
DR = pickle.load(open(inp,"rb"))

### Creates a function to do hierarchical clustering on the dimensionality reduction
def HierClust(data,clusters=50,metric="euclidean",linkage='average'):
    clustering = AgglomerativeClustering(n_clusters=clusters, metric=metric, linkage=linkage)
    cluster_labels = clustering.fit_predict(data.T)
    df=pd.DataFrame(columns=["x","y","c"])
    df.x=data[0]
    df.y=data[1]
    df.c=cluster_labels
    return df

### Creates an empty DICT variable, then fills it with the cluster labels for each DR feature, perplexity, and at varying cluster sizes.
INFO={}
for dr in LINEAR.keys():
    INFO[dr]={}
    if dr in ["tica"]:
        for feat in ["phipsi","distang","sasa"]: # LINEAR[dr].keys():
            INFO[dr][feat]={}
            for n_clust in np.concatenate([np.arange(2,10),np.arange(10,100,10),np.arange(100,500,100)]):
                INFO[dr][feat][n_clust]={}
                INFO[dr][feat][n_clust]["CL"]=HierClust(LINEAR[dr][feat].T[::10].T,n_clust)
                INFO[dr][feat][n_clust]["DB"]=metrics.davies_bouldin_score(LINEAR[dr][feat].T[::10], INFO[dr][feat][n_clust]["CL"].c)
                INFO[dr][feat][n_clust]["SS"]=metrics.silhouette_score(LINEAR[dr][feat].T[::10], INFO[dr][feat][n_clust]["CL"].c, metric='euclidean')
    if dr in ["tsne"]:
        for perp in LINEAR[dr].keys():
            print()
            INFO[dr][perp]={}
            for feat in LINEAR[dr][perp].keys():
                INFO[dr][perp][feat]={}
                for n_clust in np.concatenate([np.arange(2,10),np.arange(10,100,10),np.arange(100,500,100)]):
                    INFO[dr][perp][feat][n_clust]={}
                    INFO[dr][perp][feat][n_clust]["CL"]=HierClust(LINEAR[dr][perp][feat].T,n_clust)
                    INFO[dr][perp][feat][n_clust]["DB"]=metrics.davies_bouldin_score(LINEAR[dr][perp][feat], INFO[dr][perp][feat][n_clust]["CL"].c)
                    INFO[dr][perp][feat][n_clust]["SS"]=metrics.silhouette_score(LINEAR[dr][perp][feat], INFO[dr][perp][feat][n_clust]["CL"].c, metric='euclidean')

### Outputs the DICT variable into the pickle file for later analysis
pickle.dump(INFO,open(pkl,'wb'))
