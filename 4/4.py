import random


p_mutation = 0.2
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''
    child = []
    crossoverPoint = random.randint(0, len(mother)-1)
    child.extend(mother[:crossoverPoint] + father[crossoverPoint:])
    return tuple(child)


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    mutated = list(individual)
    bit = random.randint(0, len(individual)-1)
    mutated[bit] = (mutated[bit] - 1) * (- 1)
    return tuple(mutated)


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.
    totalFitness = 0
    selected = set()

    orderedPopulation = list(population)

    for individual in orderedPopulation:
        totalFitness += fitness_function(individual)

    while len(selected) < 2:
        for individual in orderedPopulation:
            if random.randint(0, 100) < (fitness_function(individual) / totalFitness) * 100:
                selected.add(individual)

    return selected.pop(), selected.pop()


def fitness_function(individual):
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual
    '''
    fitness = 0
    pairs = enumerate(reversed(individual))

    for pair in pairs:
        fitness += (pair[0] + 1) * pair[1]

    return fitness
    '''
    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }
    #initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(
        initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
