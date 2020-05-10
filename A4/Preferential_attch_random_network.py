import networkx as nx
import matplotlib.pyplot as plt
from random import sample, random
import math
import numpy as np
import collections

# Code ready to run
# susceptible (0), infected (1)

class Draw:
    def __init__(self, G):
        self.G = G
        self.pos = nx.spring_layout(G)  # to nicely plot the population

    def plot_population(self, state):
        nx.draw_networkx_nodes(self.G, self.pos,
                               nodelist=infected_nodes(state, self.G.nodes()),
                               node_color='r',
                               node_size=100,
                               alpha=0.8)
        nx.draw_networkx_nodes(self.G, self.pos,
                               nodelist=susceptible_nodes(state, self.G.nodes()),
                               node_color='b',
                               node_size=100,
                               alpha=0.8)
        nx.draw_networkx_edges(self.G, self.pos, width=1.0)
        plt.draw()
# end of class Draw

def infected_nodes(state, sample):
    # get list of nodes that are infected
    return list(filter(lambda j: state[j] == 1, sample))


def susceptible_nodes(state, sample):
    # get list of nodes that are susceptible
    return list(filter(lambda j: state[j] == 0, sample))


def p_infected(const_p, n):
    # compute probility of getting infected having n infected neighbors
    return 1 - math.exp(-const_p*n)


def simulate_disease(G, state, const_p, r, t_steps):
    # simulate the disease for t_steps and graph G with intial state given by
    # state, and constant parameters const_p and r
    # returns an array of infected individuals in each day
    new = np.zeros(len(state))
    I_count = np.zeros(t_steps+1)
    for t in range(t_steps):
        I_count[t] = sum(state)
        for i in G.nodes():
            if state[i] == 1:
                new[i] = 1 - int(random() < r)
                continue
            n = len(infected_nodes(state, G.neighbors(i)))
            new[i] = int(random() < p_infected(const_p, n))
        state = new.copy()

    I_count[t_steps] = sum(state)
    return I_count


# #######Task3 ######## #
#Read_ME:
#1.For the results n2=5000 nodes were used
#2. If we want to see nice plots in less time we can use n1
        



#Return random graph using Barabási-Albert preferential attachment model.
n1=1000  #nodes first try
n2=5000 #node second try
m=1     #Number of edges to attach from a new node to existing nodes

G_r=nx.barabasi_albert_graph(n1,m) #####CHANGE IN n2 if necessary###########

nx.draw(G_r, node_color='orange', node_size=30, edge_color='black', linewidths=1, font_size=15)
plt.show()

#plot a histogram of the degree distribution on a normal scale
degree_sequence = sorted([d for n, d in G_r.degree()], reverse=True)  # degree sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())
fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')
plt.title("Degree Histogram on Preferential attachement Random Graph")
plt.ylabel("number of nodes")
plt.xlabel("Degree")
plt.show()


#Average degree of the network
avg_deg = 2 * nx.number_of_edges(G_r) / nx.number_of_nodes(G_r)
print("Average degree:", avg_deg)


#plot a histogram of the degree distribution on log-log scale
dmax=max(degree_sequence)
print("max degree=",dmax)
plt.loglog(degree_sequence,'b-',marker='o')
plt.title("Degree plot on Preferential attachement Random Graph (log scale)")
plt.ylabel("degree")
plt.xlabel("number of nodes")
plt.show()


# ######### Task 4 ############ #
#Repeate task 2 on preferenced attachement network

r = 0.03  # prob with which an I recovers (becomes S) (per day)
I_0_count = 100  # how many I are there at t=0
t_steps = 1000   #simulation days
p_values = np.arange(0.001, 0.011, 0.001)  # constants p used in the experiment
last_day_stats = np.zeros(len(p_values))

state0 = np.zeros(n2) 
infected = sample(list(G_r.nodes()), I_0_count) 
state0[infected] = 1 #randomly placed infected

for i, p_const in enumerate(p_values):
    state=state0.copy()
    I_r_count=simulate_disease(G_r,state,p_const,r,t_steps)
    last_day_stats[i] = I_r_count[-1]
    label = "p = " + str(round(p_const, 3))
    plt.plot(I_r_count, label=label)

print(last_day_stats)
plt.xlabel('Time steps')
plt.ylabel('Number of infected')
plt.legend()

plt.figure(2)
plt.plot([r/p for p in p_values], last_day_stats,color='blue', marker='o')
plt.xlabel('r/p')
plt.ylabel('Number of infected')

plt.show()

# To plot a population:
draw_G = Draw(G_r)
draw_G.plot_population(state)
plt.show()





    





