from ga_clustering import *
import numpy as np
import sys

if len(sys.argv) > 1 and len(sys.argv) < 4:
    print('Either run with no paramenters to generate a dataset'
          ' or provide: dataset_fn K P')
    sys.exit(1)

output_dir = "."
if len(sys.argv) > 1:
    dataset = np.load(sys.argv[1])
    K = int(sys.argv[2])
    P = int(sys.argv[3])
    n, dim = dataset.shape
    if len(sys.argv) > 4:
        output_dir = sys.argv[4]
else:
    K = 8  # number of clusters
    P = 100  # population size
    dim = 2
    n = 2000
    (dataset, clusters) = dataset_with_noise(n, dim, K, noise=0.15)


steps = 100  # number of generations
mu_c = 0.8  # probability of a crossover
mu_m = 0.01  # probability of a mutation

(avg_fitness, gen_similarity, best_fitness, best_individual, generation, t_steps) =\
    ga_clustering(dataset, K, P, steps, mu_c, mu_m,
                  crossover_fn=heuristic_crossover, adaptive_params=True,
                  selection_fn=roulette_wheel_selection, printing=True)

M = 1/best_fitness  # curly M of the best individual

best_ind_fn = output_dir + "/best_individual.npy"
avg_fitness_fn = output_dir + "/avg_fitness.npy"
gen_similarity_fn = output_dir + "/gen_similarity.npy"
generation_fn = output_dir + "/generation.npy"
dataset_fn = output_dir + "/dataset.npy"

print("Score of the best individual:", best_fitness, " curly M =", M)
print("Stopped after %d steps" % (t_steps+1))

print("Saving results in %s, %s, %s, %s, %s" %
      (best_ind_fn, avg_fitness_fn, generation_fn,
       gen_similarity_fn, dataset_fn))

np.save(best_ind_fn, best_individual)
np.save(avg_fitness_fn, avg_fitness)
np.save(generation_fn, generation)
np.save(gen_similarity_fn, gen_similarity)
np.save(dataset_fn, dataset)
