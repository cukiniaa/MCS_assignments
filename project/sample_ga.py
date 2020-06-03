from ga_clustering import ga_clustering, clustered_dataset, dataset_with_noise
import numpy as np
import sys

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
    K = 6  # number of clusters
    P = 100  # population size
    dim = 2
    n = 1000
    # (dataset, clusters, centers) = clustered_dataset(n, dim, K)
    (dataset, clusters, centers) = dataset_with_noise(n, dim, K, noise=0.2)
    # dataset, _ = clustered_dataset(n, dim, K, True)  # moon-like data

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

# Notes from our zoom
# mu_m_values = array of values
# mu_count = mu_m_values.shape[0]
# M = np.zeros((mu_count, n_tries))
# 
# for j in range(0, mu_count):
#     for i in range(0, 10):
#         (avg_fitness, best_fitness, best_individual, generation) =
#         ga_clustering(dataset, K, P, steps, mu_c, mu_m)
#         M[j][i] = 1/best_fitness
# 
# np.save("M", M)
