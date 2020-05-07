#! /usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.centrality import betweenness_centrality
from operator import itemgetter
import collections


def degree_histogram(G, title="Degree Histogram", fig=1):
    degree_sequence = sorted([d for n, d in G.degree()],
                             reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.figure(fig)
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title(title)
    plt.ylabel("Number of nodes")
    plt.xlabel("Degree")
    plt.xlim(right=35)
    plt.tight_layout()
    plt.draw()


def betweenness_plot(G, title="", fig=1):
    y = sorted(betweenness_centrality(G).items(), key=itemgetter(1),
               reverse=True)
    y = [(G.degree(n), bc) for n, bc in y]
    deg, bc = zip(*y)
    plt.figure(fig)
    plt.plot(bc, deg, 'o')
    plt.title(title)
    plt.xlabel("Betweenness Centrality")
    plt.ylabel("Degree of node")
    plt.ylim(top=35)
    plt.xlim(right=0.4)
    plt.tight_layout()
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

# ### Stats of the real network

betweenness_plot(G, fig=1, title="The Real Network")
degree_histogram(G, fig=2, title="The Real Network")


# ### Stats of a random graph

def create_binomial(G):
    V_size = G.number_of_nodes()
    E_size = G.number_of_edges()
    p = 2 * E_size / (V_size * (V_size - 1))
    return nx.gnp_random_graph(V_size, p)


Gr = create_binomial(G)
betweenness_plot(Gr, fig=3, title="A binomial graph")
degree_histogram(Gr, fig=4, title="A binomial graph")


# ### Stats of a random graph, generated with preferential attachment

def create_ba_graph(G):
    V_size = G.number_of_nodes()
    return nx.barabasi_albert_graph(V_size, 2)


Gb = create_ba_graph(G)
betweenness_plot(Gb, fig=5, title="A Barabasi-Albert Graph")
degree_histogram(Gb, fig=6, title="A Barabasi-Albert Graph")

plt.show()
