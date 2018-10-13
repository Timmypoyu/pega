import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, fcluster 
from scipy.spatial.distance import pdist
import numpy as np 
import csv 
import pandas as pd


#reader = csv.reader(open("final.csv", "rb"), delimiter=",")
#print(reader)
#x = list(reader)
#print(x)
#result = np.array(reader.drop(['Config'], 1).astype(float))
#print(result)
train = pd.read_csv('./final.csv')
df = train.set_index('Config')
del df.index.name

X = np.array(train.drop(['Config'], 1).astype(float))
#print(len(X))
Z = linkage(X, 'ward')
#print(len(Z))
#print(Z[:20])


#c, coph_dists = cophenet(Z, pdist(X))
#
#plt.figure(figsize=(100,80))
#plt.scatter(X[:,0], X[:,1], X[:,2], X[:,3])
#plt.show()
#plt.savefig('table22.png')

max_d = 30000
clusters = fcluster(Z, max_d, criterion='distance')
print("max:" + str(max_d))
print(clusters)



#plt.figure(figsize=(50,20))
#plt.title('Hierarchial Clustering Dendrogram')
#plt.xlabel('sample index')
#dendrogram(
#	Z,
#	leaf_rotation=90.,
#	leaf_font_size=6.,
#	labels=df.index
#)
#plt.show()
#plt.savefig('dendro_refined.png')
