#! /usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from networkx.algorithms.centrality import betweenness_centrality
from operator import itemgetter


# functions responsible for choosing a node to delete
choose_random = lambda G: random.choice(list(G.nodes()))
highest_deg_node = lambda G: max(list(G.degree()), key=itemgetter(1))[0]
max_betweenness = lambda G: max(betweenness_centrality(G).items(),
                                key=itemgetter(1))[0]


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


def mccs_experiment(G, alphas, n_tries, node_choice_func, graph_create):
    """A function to run an experiment for graph G and
    different values of alpha (proportion of nodes to remove),
    it computes a average max connected component size fom n_tries,
    for each alpha in alphas as return a list of mccs."""
    mccs = np.zeros(len(alphas))
    for i, alpha in enumerate(alphas):
        for j in range(n_tries):
            Gc = graph_create(G)
            remove_nodes(Gc, alpha, node_choice_func)
            mccs[i] += mcc_size(Gc)

    mccs /= n_tries
    return mccs


def test_graph(G, alphas, n_tries, graph_create):
    print("Random")
    mccs_random = mccs_experiment(G, alphas, n_tries, choose_random,
                                  graph_create)
    print(mccs_random)
    print("Highest deg")
    mccs_highest_deg = mccs_experiment(G, alphas, n_tries, highest_deg_node,
                                       graph_create)
    print(mccs_highest_deg)
    print("Betweenness")
    mccs_betweenness = mccs_experiment(G, alphas, n_tries, max_betweenness,
                                       graph_create)
    print(mccs_betweenness)
    return (mccs_random, mccs_highest_deg, mccs_betweenness)


def plot_result(res, fig=1, title=""):
    (mccs_random, mccs_highest_deg, mccs_betweenness) = res
    plt.figure(fig)
    plt.plot(alphas, mccs_random, label="random")
    plt.plot(alphas, mccs_highest_deg, label="highest degree")
    plt.plot(alphas, mccs_betweenness, label="highest betweeness centrality")
    plt.xlabel(r'$\alpha$')
    plt.ylabel("Max connected component size")
    plt.title(title)
    plt.legend()
    plt.draw()


# ### Read in the real network

df = open("ca-netscience.mtx", 'r')

line = df.readline()  # read in a comment
line = df.readline().strip().split()  # read in metadata about the network
V_size = int(line[1])
E_size = int(line[3])

print("Real network: |V| = %d, |E| = %d" % (V_size, E_size))

G = nx.empty_graph(V_size)
for line in df:
    edge = tuple(int(node)-1 for node in line.strip().split())
    G.add_edge(*edge)

# ###

alphas = [0.001, 0.01, 0.025, 0.05, 0.055, 0.06, 0.07, 0.08, 0.1, 0.12, 0.2, 0.3]
n_tries = 1

# ### Test the real network
# NOTE: For the real network there's no point to run the highest deg test nor
# betweenness test multiple times because they always generate the same results
# test_graph wasn't used in this case

print("\nReal network experiment...")

print("Random")
mccs_rand = mccs_experiment(G, alphas, n_tries, choose_random, lambda G: G.copy())
print(mccs_rand)

print("Highiest deg")
mccs_highest_deg = mccs_experiment(G, alphas, 1, highest_deg_node, lambda G: G.copy())
print(mccs_highest_deg)

print("Betweenness")
mccs_betweenness = mccs_experiment(G, alphas, 1, max_betweenness, lambda G: G.copy())
print(mccs_betweenness)


res = (mccs_rand, mccs_highest_deg, mccs_betweenness)
plot_result(res, fig=1, title="Real network")


# ### Test a random graph

def create_binomial(G):
    V_size = G.number_of_nodes()
    E_size = G.number_of_edges()
    p = 2 * E_size / (V_size * (V_size - 1))
    return nx.gnp_random_graph(V_size, p)


print("\nRandom (binomial) experiment...")
res = test_graph(G, alphas, n_tries, create_binomial)
plot_result(res, fig=2, title="A binomial graph")


# ### Test a random graph, generated with preferential attachment

def create_ba_graph(G):
    V_size = G.number_of_nodes()
    return nx.barabasi_albert_graph(V_size, 2)


print("\nBarabasi-Albert experiment")
res = test_graph(G, alphas, n_tries, create_ba_graph)
plot_result(res, fig=3, title="A Barabasi-Albert graph")

plt.show()
