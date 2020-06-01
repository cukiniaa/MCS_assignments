#!/usr/bin/python3
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from mpl_toolkits.mplot3d import Axes3D
# plt.rcParams.update({'font.size': 20})

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print('Run: python3 %s dataset_fn chromosome_fn \n'
              'filenames are expected to be .npy,'
              ' (ex. dataset.npy best_individual.npy).' % (sys.argv[0]))
        sys.exit(1)

    dataset = np.load(sys.argv[1])  # load dataset
    chromosome = np.load(sys.argv[2])  # load chromosome
    N, dim = dataset.shape
    K = len(chromosome) // dim

    print("Dataset with %d points, dim = %d, K = %d" % (N, dim, K))

    if dim > 3:
        print("Dataset of dimension > 3, plotting 3D.")

    centers = chromosome.reshape(K, dim)
    distances = cdist(dataset, centers)
    clusters = np.argmin(distances, axis=1)

    if dim == 2:
        plt.scatter(dataset[:, 0], dataset[:, 1], c=clusters)
    else:
        ax = plt.subplot(111, projection='3d')
        ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], c=clusters)

    plt.tight_layout()
    plt.show()
