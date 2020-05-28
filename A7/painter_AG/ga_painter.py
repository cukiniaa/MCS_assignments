from painter_play import painter_play
import numpy as np
from bisect import bisect_left


def initialize_population(P):
    chromosomes = np.random.randint(0, 4, (54, P))
    return chromosomes


def individual_fitness(chromosome, room):
    n_tries = 10
    fitness = 0
    for i in range(0, n_tries):
        f, _, _ = painter_play(chromosome, room)
        fitness += f
    return fitness / n_tries


def population_fitness(chromosomes, room):
    P = chromosomes.shape[1]
    fitness = np.zeros(P)
    for i in range(0, P):
        fitness[i] = individual_fitness(chromosomes[:, i], room)
    return fitness


def select(chromosomes, fitness):
    P = chromosomes.shape[1]
    new_generation = np.zeros((54, P))
    f_sum = np.sum(fitness)
    ind_ord = np.argsort(fitness)
    f_sorted = np.take_along_axis(fitness, ind_ord, axis=0)
    prob = np.add.accumulate(f_sorted / f_sum)  # accumulated probability
    for i in range(0, P):  # choose P chromosomes from the previous generation
        r = np.random.random()
        ind = bisect_left(prob, r)  # which probability is chosen
        ind = ind_ord[ind]  # which chromosome is chosen
        new_generation[:, i] = np.copy(chromosomes[:, ind])
    return new_generation


def crossover(chromosomes, miu_c):
    P = chromosomes.shape[1]
    for i in range(0, P - P % 2, 2):  # mutation for parents i, i+1
        if np.random.random() > miu_c:
            continue
        ind = np.random.randint(0, 54)  # swap elements starting from ind
        chromosomes[ind:, i], chromosomes[ind:, i+1] = np.copy(chromosomes[ind:, i+1]), np.copy(chromosomes[ind:, i])


def mutation(chromosomes, miu_m):
    P = chromosomes.shape[1]
    for i in range(0, P):
        if np.random.random() > miu_m:
            continue
        ind = np.random.randint(0, 54)  # which position is mutated
        prev_val = chromosomes[ind][i]
        while (new_val := np.random.randint(0, 4)) == prev_val:
            continue
        chromosomes[ind][i] = new_val


P = 50  # population size
room = np.zeros((20, 40))  # room to paint
steps = 200  # number of generations
miu_c = 0.2  # probability of a crossover
miu_m = 0.2  # probability of a mutation

best_fitness = 0
best_individual = None

population = initialize_population(P)
for t in range(0, steps):
    fitness = population_fitness(population, room)
    ind = np.argmax(fitness)
    print("Best fitness:", fitness[ind])
    if fitness[ind] > best_fitness:
        best_fitness = fitness[ind]
        best_individual = np.copy(population[:, ind])
    population = select(population, fitness)
    crossover(population, miu_c)
    mutation(population, miu_m)

print("\nBest fitness overall:", best_fitness)
print("Testing the best individual:")
for i in range(0, 5):
    print("Fitness:", painter_play(best_individual, room)[0])
