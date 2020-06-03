import numpy as np
from bisect import bisect_left
from scipy.spatial.distance import cdist
from sklearn.datasets import make_blobs, make_moons


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

def single_point_crossover(generation, copy_factor, mu_c):
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

def double_point_crossover(generation, copy_factor, mu_c):
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
        ind_1=np.random.randint(1, length-1)
        ind_2=np.random.randint(1, length-1)
        while ind_1 > ind_2:
            ind_2=np.random.randint(1, length-1)
       
        new_generation[i, :ind_1] = generation[p1, :ind_1]
        new_generation[i, ind_1:] = generation[p2, ind_1:]
        new_generation[i, ind_2:] = generation[p1, ind_2:]
        
        new_generation[i+1, :ind_1] = generation[p2, :ind_1]
        new_generation[i+1, ind_1:] = generation[p1, ind_1:]
        new_generation[i+1, ind_2:] = generation[p2, ind_2:]
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




def clustered_dataset(n, dim, centers, moons=False):
    # centers can be either integer K or a list of centers coords
    # return make_blobs(n_samples=n, n_features=dim,
    if moons:
        return make_moons(n, noise=0.1)
    return make_blobs(n_samples=n, n_features=dim,centers=centers)


def dataset_with_noise(n, dim, centers, noise=0.1):
    N = int((1 - noise) * n)
    d = np.zeros((n, dim))
    cl = np.zeros(n)
    (d[:N, :], cl[:N]) = make_blobs(n_samples=N, n_features=dim, centers=centers)
    d[N:, :] = -10 + 20 * np.random.rand(n-N, dim)
    return (d, cl)


def random_dataset(n, dim):
    return 10 * np.random.rand(n, dim)


def ga_clustering(dataset, K, P, steps, mu_c, mu_m,
                  crossover_fn=double_point_crossover,
                  printing=False):
    n, dim = dataset.shape
    best_fitness = 0
    best_individual = None
    avg_fitness = np.zeros(steps)

    if printing:
        print('GA with K = %d, P = %d, n = %d, dim = %d, steps = %d,'
              ' mu_c = %.3f, mu_m = %.3f' % (K, P, n, dim, steps, mu_c, mu_m))

    generation = initialize_population(dataset, K, P)
    for t in range(0, steps):
        fitness = population_fitness(generation, dataset, K)
        avg_fitness[t] = np.average(fitness)
        if (printing and t % 10 == 0):
            print("Avg fitness:", avg_fitness[t])
        ind = np.argmax(fitness)
        if fitness[ind] > best_fitness:
            best_fitness = fitness[ind]
            best_individual = np.copy(generation[ind, :])
        copy_factor = select(generation, fitness)
        generation = crossover_fn(generation, copy_factor, mu_c)
        mutation(generation, mu_m)

    return (avg_fitness, best_fitness, best_individual, generation)



















