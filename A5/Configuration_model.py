
import random
import community as community_louvain
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import community

#Code ready to run.

net_1 = open("/Users/charitinistavropoulou/Documents/Python_MCS_ass5/Facebook_messages.txt", 'r')

#1.Generate the degree sequence of a real network : Facebook messages
def degree_seq(net):
    lines=net.readlines()
    num_vertices=lines[1].split()[0]
    num_edges=lines[1].split()[2]
    G=nx.empty_graph(num_vertices)

    for i in range(2,len(lines)):
        G.add_edge(lines[i].split()[0],lines[i].split()[1])

    #generate degree sequence
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)

    return degree_sequence

deg_seq=degree_seq(net_1)

#3.By repeated simulations, (≥ 30), record the values
#of the global clustering coefficient on the random graph

def experiment(n_tries):

    samples=5
    G_list=list()
    #array to hold the average_clustering coeff for all the n_tries
    data=np.zeros(n_tries)
    for i in range(n_tries):
        for j in range(samples):
            G=nx.configuration_model(deg_seq)
            G=nx.Graph(G)
            G_list.append(G)
        G=random.choice(G_list)
        average_clustering= nx.average_clustering(G)
        data[i]=average_clustering
    
    return data


my_data=experiment(50) #50 simulations
av_clustering_relNet=0.068 #take one global clust coeff from previous ex: Facebook_messages 
fig1,fig2=plt.subplots()

#Ancomment if we want on the same fig the statistic of the real net
#fig2=plt.boxplot(av_clustering_relNet)

fig1=plt.boxplot(my_data)
x = np.random.normal(1, 0.04, size=len(my_data))
plt.plot(x,my_data,'r.',alpha=0.5)
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
   



