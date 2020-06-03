from ga_cluster  import clustered_dataset, initialize_population, population_fitness, select, crossover,mutation
import random
import numpy as np
from bisect import bisect_left
from scipy.spatial.distance import cdist
import sys
import matplotlib.pyplot as plt


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

steps = 100 # number of generations
mu_c = 0.8  # probability of a crossover

#vary the mutation rate by creating a mu_m list

mut_exp=20
prob=[]
for i in range(mut_exp):
    r=random.uniform(0,1)  #make it smaller
    prob.append(r)
    
mu_m=sorted(list(set(prob)))
best_fitness = 0
best_individual = None
avg_fitness = np.zeros(steps)

generation = initialize_population(dataset, K, P)
fit=[]

for i in mu_m:
  
    for t in range(0, steps):
        fitness = population_fitness(generation, dataset, K)[0]
        avg_fitness[t] = np.average(fitness)
        #if (t % 10 == 0):
            #print("Avg fitness:", avg_fitness[t])
        ind = np.argmax(fitness)
        if fitness[ind] > best_fitness:
            best_fitness = fitness[ind]
            best_individual = np.copy(generation[ind, :])
        copy_factor = select(generation, fitness)
        generation = crossover(generation, copy_factor, mu_c)
        mutation(generation,i)
    fit.append(best_fitness)

np.save()
for i in range(len(mu_m)):
    print("fitness ", fit[i], "mutation rate", mu_m[i])





plt.xlabel('Probability of Mutation')
plt.ylabel('Max Average Fitness ')





plt.show()



    
