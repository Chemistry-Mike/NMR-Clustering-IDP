### 
import pickle
import numpy as np
import sys
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn import metrics

### 
HOME="/mnt/proj1/open-27-2/bakkerm/"

### 
protein="pDp53"

inp = HOME+"6-Conda/1-PICKLES/DR/"+protein+"-DimRed.pkl"
pkl = HOME+"6-Conda/1-PICKLES/CLUSTS/"+protein+"-cluster.pickle"

def HierClust(data,clusters=50,metric="euclidean",linkage='average'):
    clustering = AgglomerativeClustering(n_clusters=clusters, metric=metric, linkage=linkage)
    cluster_labels = clustering.fit_predict(data.T)
    df=pd.DataFrame(columns=["x","y","c"])
    df.x=data[0]
    df.y=data[1]
    df.c=cluster_labels
    return df

DR = pickle.load(open(inp,"rb"))

INFO={}
pickle.dump(INFO,open(pkl,'wb'))
for dr in LINEAR.keys():
    INFO[dr]={}
    if dr in ["tica"]:
        print(LINEAR[dr].keys())
        for feat in ["phipsi","distang","sasa"]: # LINEAR[dr].keys():
            print(feat)
            INFO[dr][feat]={}
            for n_clust in np.concatenate([np.arange(2,10),np.arange(10,100,10),np.arange(100,500,100)]):
                INFO[dr][feat][n_clust]={}
                INFO[dr][feat][n_clust]["CL"]=HierClust(LINEAR[dr][feat].T[::10].T,n_clust)
                INFO[dr][feat][n_clust]["DB"]=metrics.davies_bouldin_score(LINEAR[dr][feat].T[::10], INFO[dr][feat][n_clust]["CL"].c)
                INFO[dr][feat][n_clust]["SS"]=metrics.silhouette_score(LINEAR[dr][feat].T[::10], INFO[dr][feat][n_clust]["CL"].c, metric='euclidean')
        pickle.dump(INFO,open(pkl,'wb'))
    if dr in ["tsne"]:
        continue
        print(LINEAR[dr].keys())
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

pickle.dump(INFO,open(pkl,'wb'))
