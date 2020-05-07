import random
import community as community_louvain
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import community


#By reapeted simulations>=30 record the values of the average clustering coeff
#illustrate using a box and a whisker plot and show on the same plot
#the value of average clustering on the example network

def experiment(n_tries):
    p=0.006
    num_nodes=1266
    #array to hold the average_clustering coeff for all the n_tries
    data=np.zeros(n_tries)
    for i in range(n_tries):
        G_ER=nx.erdos_renyi_graph(num_nodes,p)
        average_clustering=nx.average_clustering(G_ER)
        data[i]=average_clustering
    return data

my_data=experiment(50) #50 simulations
av_clustering_relNet=0.068 #take one global clust coeff from previous ex: Facebook_messages 
fig1,fig2=plt.subplots()
fig2=plt.boxplot(av_clustering_relNet)
fig1=plt.boxplot(my_data)
plt.show()

#Was the global clust coeff on the real-network greater then 95%
#of the values of the global clust coeff which you recorded for the random graphs?
sample_size=int ((95 *len(my_data))/100)
sample=np.random.choice(my_data,sample_size)
c=0
for i in sample: 
    if i<av_clustering_relNet:
        c+=1

if c==sample_size:
    print("The global clustering coeff on the real-network is greater than the 95% of the values of the global clust coeff that were recorded for the random graphs")
   

    
    
