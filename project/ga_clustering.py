import numpy as np
from bisect import bisect_left
from scipy.spatial.distance import cdist
import sys


def initialize_population(dataset, K, P):
    N, dim = dataset.shape
    ind = np.random.randint(0, N, K*P)
    return dataset[ind, :].reshape(P, dim*K)


def population_fitness(chromosomes, dataset, K):
    P = chromosomes.shape[0]
    N, dim = dataset.shape
    fitness = np.zeros(P)
    for i in range(0, P):
        centers = chromosomes[i, :].reshape(K, dim)  # of the i-th individual
        distances = cdist(dataset, centers)  # distances of each point to each center
        clusters = np.argmin(distances, axis=1)  # each point gets assigned a cluster index
        new_centers = np.copy(centers)  # will hold mean points of respective clusters

        M = 0
        for j in range(0, K):
            cluster = np.array(clusters == j)
            c_dataset = dataset[cluster, :]
            if c_dataset.shape[0] == 0:
                continue
            c_j = np.sum(c_dataset, axis=0)
            new_centers[j, :] = c_j / c_dataset.shape[0]  # mean point of cluster j
            M += np.sum(np.linalg.norm(c_dataset - new_centers[j, :], axis=1))
            # sum of distances from the new center to all points in cluster j

        chromosomes[i, :] = new_centers.flatten()  # update chromosome
        fitness[i] = 1/M
    return fitness


def select(chromosomes, fitness):
    # select parents using the roulette wheel,
    # number of copies of each chromosome will be return
    # chromosomes are not changed in any way
    P = chromosomes.shape[0]
    copy_factor = np.zeros(P)
    f_sum = np.sum(fitness)
    ind_ord = np.argsort(fitness)
    f_sorted = np.take_along_axis(fitness, ind_ord, axis=0)
    prob = np.add.accumulate(f_sorted / f_sum)  # accumulated probability
    for i in range(0, P):  # choose P chromosomes from the previous generation
        r = np.random.random()
        ind = bisect_left(prob, r)  # which probability is chosen
        ind = ind_ord[ind]  # which chromosome is chosen
        copy_factor[ind] += 1
    return copy_factor


def crossover(generation, copy_factor, mu_c):
    P, length = generation.shape
    new_generation = np.zeros((P, length))
    parent_index = np.add.accumulate(copy_factor)

    for i in range(0, P - P % 2, 2):
        [r1, r2] = np.random.randint(1, P+1, 2)
        p1 = bisect_left(parent_index, r1)
        p2 = bisect_left(parent_index, r2)
        if np.random.random() > mu_c:  # no crossover
            new_generation[i, :] = generation[p1, :]
            new_generation[i+1, :] = generation[p2, :]
            continue
        ind = np.random.randint(1, length-1)  # swap elements starting from ind
        new_generation[i, :ind] = generation[p1, :ind]
        new_generation[i, ind:] = generation[p2, ind:]
        new_generation[i+1, :ind] = generation[p2, :ind]
        new_generation[i+1, ind:] = generation[p1, ind:]

    return new_generation


def mutation(chromosomes, mu_m):
    # in place mutation with probability mu_m
    P, length = chromosomes.shape
    for i in range(0, P):
        if np.random.random() > mu_m:
            continue
        ind = np.random.randint(0, length)  # which position is mutated
        delta = np.random.rand()
        sign = 1 - 2 * (np.random.rand() > 1/2)
        prev_value = chromosomes[i][ind]
        chromosomes[i][ind] = 2 * delta * (prev_value or 1) * sign


def clustered_dataset(n, dim, K):
    dataset = np.zeros((n, dim))
    rand = np.random.rand(n, dim) + 1
    ind = np.zeros(K+1)
    ind[1:K] = np.random.randint(1, n, K-1)
    ind[K] = n
    ind = np.sort(ind).astype(int)
    for i in range(1, K+1):
        d = np.random.randint(1, 10)
        R = d * (np.random.rand(1, dim) + 1)
        dataset[ind[i-1]:ind[i], :] = R +\
                d * (1 + np.random.rand()) * rand[ind[i-1]:ind[i], :]
    return dataset


def random_dataset(n, dim):
    return 10 * np.random.rand(n, dim)


def ga_clustering(dataset, K, P, steps, mu_c, mu_m):
    best_fitness = 0
    best_individual = None
    avg_fitness = np.zeros(steps)

    print('GA with K = %d, P = %d, n = %d, dim = %d, steps = %d, mu_c = %.3f,'
          ' mu_m = %.3f' % (K, P, n, dim, steps, mu_c, mu_m))

    generation = initialize_population(dataset, K, P)
    for t in range(0, steps):
        fitness = population_fitness(generation, dataset, K)
        avg_fitness[t] = np.average(fitness)
        if (t % 10 == 0):
            print("Avg fitness:", avg_fitness[t])
        ind = np.argmax(fitness)
        if fitness[ind] > best_fitness:
            best_fitness = fitness[ind]
            best_individual = np.copy(generation[ind, :])
        copy_factor = select(generation, fitness)
        generation = crossover(generation, copy_factor, mu_c)
        mutation(generation, mu_m)

    return (avg_fitness, best_fitness, best_individual, generation)


if len(sys.argv) > 1 and len(sys.argv) < 4:
    print('Either run with no paramenters to generate a dataset'
          ' or provide: dataset_fn K P')
    sys.exit(1)

if len(sys.argv) > 1:
    dataset = np.load(sys.argv[1])
    K = int(sys.argv[2])
    P = int(sys.argv[3])
    n, dim = dataset.shape
else:
    K = 2  # number of clusters
    P = 100  # population size
    dim = 3
    n = 1000
    dataset = clustered_dataset(n, dim, K)

steps = 100  # number of generations
mu_c = 0.8  # probability of a crossover
mu_m = 0.01  # probability of a mutation

(avg_fitness, best_fitness, best_individual, generation) =\
    ga_clustering(dataset, K, P, steps, mu_c, mu_m)

M = 1/best_fitness  # curly M of the best individual

best_ind_fn = "best_individual.npy"
avg_fitness_fn = "avg_fitness.npy"
generation_fn = "generation.npy"
dataset_fn = "dataset.npy"

print("Score of the best individual:", best_fitness, " curly M =", M)

print("Saving results in %s, %s, %s, %s" %
      (best_ind_fn, avg_fitness_fn, generation_fn, dataset_fn))

np.save(best_ind_fn, best_individual)
np.save(avg_fitness_fn, avg_fitness)
np.save(generation_fn, generation)
np.save(dataset_fn, dataset)
