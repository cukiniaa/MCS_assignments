
import random
import community as community_louvain
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import community

#Code Ready to run.

#network_examples: Facebook_messages /emails/ physical_human_contact
net_1 = open("/Users/charitinistavropoulou/Documents/Python_MCS_ass5/Facebook_messages.txt", 'r')
net_2 = open ("/Users/charitinistavropoulou/Documents/Python_MCS_ass5/emails.txt", "r")
net_3 = open ("/Users/charitinistavropoulou/Documents/Python_MCS_ass5/ia-infect-dublin.mtx")

def network_func(net):
    lines=net.readlines()
    num_vertices=lines[1].split()[0]
    num_edges=lines[1].split()[2]
    G=nx.empty_graph(num_vertices)

    for i in range(2,len(lines)):
        G.add_edge(lines[i].split()[0],lines[i].split()[1])

    #1.statistic:global clustering coefficient
    average_clustering=nx.average_clustering(G)

    #2.statistic: maximum modularity
    #Compute the partition of the graph nodes which maximises the modularity
    #using the Louvain heuristic algorithm
    louvain_partition=community_louvain.best_partition(G)
    mod_max = community_louvain.modularity(louvain_partition,G)
    
    return average_clustering, mod_max

print("global clustering coefficient , maximium moduality: ",network_func(net_1))
print("global clustering coefficient , maximium moduality: ",network_func(net_2))
print("global clustering coefficient , maximium moduality: ",network_func(net_3))



    
