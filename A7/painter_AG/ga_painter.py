from painter_play import painter_play
import numpy as np
from bisect import bisect_left


def initialize_population(P):
    chromosomes = np.random.randint(0, 4, (54, P))
    return chromosomes


def individual_fitness(chromosome, room):
    n_tries = 20
    fitness = 0
    for i in range(0, n_tries):
        f = painter_play(chromosome, room)[0]
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


def crossover(parents, miu_c):
    P = parents.shape[1]
    new_generation = np.zeros((54, P))
    for i in range(0, P - P % 2, 2):
        [p1, p2] = np.random.randint(0, P, 2)
        if np.random.random() > miu_c:  # no crossover
            new_generation[:, i] = parents[:, p1]
            new_generation[:, i+1] = parents[:, p2]
        ind = np.random.randint(0, 54)  # swap elements starting from ind
        new_generation[ind:, i] = parents[ind:, p1]
        new_generation[:ind, i] = parents[:ind, p2]
        new_generation[ind:, i+1] = parents[ind:, p2]
        new_generation[:ind, i+1] = parents[:ind, p1]


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


def decorated_room(N, M, alpha=0.125):
    # N, M - shape of the room
    # alpha - the probablity of adding a furniture
    return np.random.choice([0, 1], (N, M), p=[1-alpha, alpha])


P = 50  # population size
room = np.zeros((20, 40))  # room to paint
steps = 200  # number of generations
miu_c = 0.7  # probability of a crossover
miu_m = 0.02  # probability of a mutation

best_fitness = 0
best_individual = None
avg_fitness = np.zeros(steps)

generation = initialize_population(P)
for t in range(0, steps):
    fitness = population_fitness(generation, room)
    avg_fitness[t] = np.average(fitness)
    ind = np.argmax(fitness)
    if (t % 10 == 0):
        print("Best fitness:", fitness[ind])
    if fitness[ind] > best_fitness:
        best_fitness = fitness[ind]
        best_individual = np.copy(generation[:, ind])
    generation = select(generation, fitness)
    crossover(generation, miu_c)
    mutation(generation, miu_m)

best_ind_fn = "best_individual.npy"
avg_fitness_fn = "avg_fitness.npy"
generation_fn = "generation.npy"
room_fn = "room.npy"

print("Saving results in %s, %s, %s, %s" %
      (best_ind_fn, avg_fitness_fn, generation_fn, room_fn))

np.save(best_ind_fn, best_individual)
np.save(avg_fitness_fn, avg_fitness)
np.save(generation_fn, generation)
np.save(room_fn, room)
