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
    K = 10  # number of clusters
    P = 100  # population size
    dim = 2
    n = 1000
    # (dataset, clusters, centers) = clustered_dataset(n, dim, K)
    (dataset, clusters) = dataset_with_noise(n, dim, K, noise=0.2)
    #dataset, _ = clustered_dataset(n, dim, K, True)  # moon-like data

steps = 100  # number of generations
mu_c = 0.8  # probability of a crossover

#generate list to calculate the probability of mutation
#mu_m=np.linspace(0.001, 0.2, num=10)
mu_m=np.arange(0.001, 0.2, 0.01)
mu_m=np.sort(mu_m)
mu_count=mu_m.shape[0]
print(mu_m)
print(mu_count)
n_tries=10;

M=np.zeros((mu_count, n_tries))
for i in range(mu_count):
   for j in range(n_tries):
      (avg_fitness, best_fitness, best_individual, generation) = ga_clustering(dataset, K, P, steps, mu_c, mu_m[i])
      M[i][j] = 1/best_fitness

#print(M)
ave_row=np.zeros(mu_count)
for i in range(mu_count):
    ave_row[i]=(np.sum(M, axis=1))[i]/n_tries

print(ave_row)

sum1=0
for j in range(n_tries):
    sum1+=M[0][j]
print(sum1)
np.save("M",M)






