#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
from random import sample, random
import math
import numpy as np

n = 5000
p = 0.0016
G = nx.fast_gnp_random_graph(n, p)

# ########### Task 1 ############ #

avg_deg = 2 * nx.number_of_edges(G) / nx.number_of_nodes(G)
print("Average degree:", avg_deg)

# plt.plot(nx.degree_histogram(G))
# plt.show()

# ########### Task 2 ############ #

# susceptible (0), infected (1)


def infected_nodes(state, sample):
    # get list of nodes that are infected
    return list(filter(lambda j: state[j] == 1, sample))


def susceptible_nodes(state, sample):
    # get list of nodes that are susceptible
    return list(filter(lambda j: state[j] == 0, sample))


class Draw:
    def __init__(self, G):
        self.G = G
        self.pos = nx.spring_layout(G)  # to nicely plot the population

    def plot_population(self):
        nx.draw_networkx_nodes(self.G, self.pos,
                               nodelist=infected_nodes(self.G),
                               node_color='r',
                               node_size=100,
                               alpha=0.8)
        nx.draw_networkx_nodes(self.G, self.pos,
                               nodelist=susceptible_nodes(self.G),
                               node_color='b',
                               node_size=100,
                               alpha=0.8)
        nx.draw_networkx_edges(self.G, self.pos, width=1.0)
        plt.draw()
# end of class Draw


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


r = 0.03  # prob with which an I recovers (becomes S) (per day)
I_0_count = 100  # how many I are there at t=0
t_steps = 1000
p_values = np.arange(0.001, 0.011, 0.001)  # constants used in the experiment
last_day_stats = np.zeros(len(p_values))

state0 = np.zeros(n)
infected = sample(list(G.nodes()), I_0_count)
state0[infected] = 1

for i, p_const in enumerate(p_values):
    state = state0.copy()
    I_count = simulate_disease(G, state, p_const, r, t_steps)
    last_day_stats[i] = I_count[-1]
    label = "p = " + str(round(p_const, 3))
    plt.plot(I_count, label=label)

plt.xlabel('Time steps')
plt.ylabel('Number of infected')
plt.legend()

plt.figure(2)
plt.plot([r/p for p in p_values], last_day_stats)
plt.xlabel('r/p')
plt.ylabel('Number of infected')

plt.show()

# To plot a population:
# draw_G = Draw(G)
# draw_G.plot_population()
# plt.show()
