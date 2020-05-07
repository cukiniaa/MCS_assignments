#! /usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from networkx.algorithms.cluster import clustering
from operator import itemgetter


def remove_nodes(G, alpha, choose_node):
    """Remove alpha proportion of nodes from G
    choose_node - a lambda function taking G as parameter,
    which specifies how to choose a node to be removed"""
    r = int(np.ceil(alpha * G.number_of_nodes()))  # number of nodes to remove
    if r >= G.number_of_nodes():
        G = nx.empty_graph()
    for i in range(r):
        node = choose_node(G)
        G.remove_node(node)


def mcc_size(G):
    """Compute max connected component size of graph G"""
    return len(max(nx.connected_components(G), key=len))


def mccs_experiment(G, alphas, n_tries, node_choice_func):
    """A function to run an experiment for graph G and
    different values of alpha (proportion of nodes to remove),
    it computes a average max connected component size fom n_tries,
    for each alpha in alphas as return a list of mccs."""
    mccs = np.zeros(len(alphas))
    for i, alpha in enumerate(alphas):
        for j in range(n_tries):
            Gc = G.copy()
            remove_nodes(Gc, alpha, node_choice_func)
            mccs[i] += mcc_size(Gc)

    mccs /= n_tries
    return mccs


def test_graph(G, alphas, n_tries, fig=1, title=""):
    mccs_random = mccs_experiment(G, alphas, n_tries, choose_randomly)
    mccs_highest_deg = mccs_experiment(G, alphas, n_tries, highest_deg_node)
    mccs_max_clustering = mccs_experiment(G, alphas, n_tries, max_clustering)
    mccs_min_clustering = mccs_experiment(G, alphas, n_tries, min_clustering)

    plt.figure(fig)
    plt.plot(alphas, mccs_random, label="random")
    plt.plot(alphas, mccs_highest_deg, label="highest degree")
    plt.plot(alphas, mccs_max_clustering, label="highest clustering coefficent")
    plt.plot(alphas, mccs_min_clustering, label="lowest clustering coefficent")
    plt.xlabel(r'$\alpha$')
    plt.ylabel("Max connected component size")
    plt.title(title)
    plt.legend()
    plt.show()


# ### Read in the real network

df = open("ca-netscience.mtx", 'r')

line = df.readline()  # read in a comment
line = df.readline().strip().split()  # read in metadata about the network
V_size = int(line[1])
E_size = int(line[3])

print("Initial |V| = %d, |E| = %d" % (V_size, E_size))

G = nx.empty_graph(V_size)
for line in df:
    edge = tuple(int(node)-1 for node in line.strip().split())
    G.add_edge(*edge)

# ###

choose_randomly = lambda G: random.choice(list(G.nodes()))
highest_deg_node = lambda G: max(list(G.degree()), key=itemgetter(1))[0]
max_clustering = lambda G: max(clustering(G).items(), key=itemgetter(1))[0]
min_clustering = lambda G: min(clustering(G).items(), key=itemgetter(1))[0]

alphas = [0.01, 0.1, 0.12, 0.14, 0.2, 0.3, 0.4, 0.5]
n_tries = 20

# ### Test the real network

test_graph(G, alphas, n_tries, fig=1, title="Real network")

# ### Test a random graph

p = 2 * E_size / (V_size * (V_size - 1))
Gr = nx.gnp_random_graph(V_size, p)

print("A binomial graph")
print("# nodes = %d, # edges = %d" % (Gr.number_of_nodes(),
                                      Gr.number_of_edges()))

test_graph(Gr, alphas, n_tries, fig=2, title="A binomial graph")

# ### Test a random graph, generated with preferential attachment

Gp = nx.barabasi_albert_graph(V_size, 2)

print("A Barbasi-Albert graph")
print("# nodes = %d, # edges = %d" % (Gp.number_of_nodes(),
                                      Gp.number_of_edges()))

test_graph(Gp, alphas, n_tries, fig=3, title="A Barbasi-Albert graph")
