import base
import random

POPULATION_SIZE = 50
FRAGMENTS_COUNT = 0
MUTATION_PROBABILITY = 0.01


def increase_fragments_count(fragments):
    global FRAGMENTS_COUNT
    FRAGMENTS_COUNT += len(fragments)


def generate_random_population():
    population = []
    for i in range(POPULATION_SIZE):
        population.append(
            (base.generate_random_reference_sequence(),
             base.generate_random_reference_sequence())
        )
    return population


def calculate_population_weights(population, fragments):
    population_weights = []
    for sequence_pair in population:
        weight = base.calculate_total_reference_sequences_fitness_score(
            sequence_pair[0], sequence_pair[1], fragments)
        population_weights.append(weight)
    return population_weights


def reproduce(parent1, parent2):
    n = len(parent1[0])
    first_random_index = random.randint(1, n)
    second_random_index = random.randint(1, n)
    first_child = parent1[0][:first_random_index] + \
        (parent2[0][-(n - first_random_index):]
         if first_random_index != n else '')
    second_child = parent1[1][:second_random_index] + \
        (parent2[1][-(n - second_random_index):]
         if second_random_index != n else '')
    return (first_child, second_child)


def mutate(child):
    random_index = random.randint(0, 1)
    mutated_child = [child[0], child[1]]
    mutated_child[random_index] = base.get_random_neighbour(
        child[random_index])
    return tuple(mutated_child)


def reproduce_new_population(population, fragments):
    new_population = []
    population_weights = calculate_population_weights(population, fragments)
    for i in range(len(population)):
        parent1 = random.choices(population, weights=population_weights)[0]
        parent2 = random.choices(population, weights=population_weights)[0]
        child = reproduce(parent1, parent2)
        if random.random() <= MUTATION_PROBABILITY:
            child = mutate(child)
        new_population.append(child)
    return new_population


def get_fittest_in_population(population, fragments):
    population_weights = calculate_population_weights(population, fragments)
    max_fitness = max(population_weights)
    index = [i for i, j in enumerate(
        population_weights) if j == max_fitness][0]
    return population[index], max_fitness


def search(experience_number):
    fragments = base.read_data_from_file(experience_number, 'fragment')
    increase_fragments_count(fragments)
    best_sequence_pair = {
        'score': 0
    }
    population = generate_random_population()
    for i in range(10):
        print('Generation number ' + str(i) + '...')
        population = reproduce_new_population(population, fragments)
        best, score = get_fittest_in_population(population, fragments)
        if score > best_sequence_pair['score']:
            best_sequence_pair['first'] = best[0]
            best_sequence_pair['second'] = best[1]
            best_sequence_pair['score'] = score
    haplotypes = base.read_data_from_file(experience_number, 'haplotype')
    print('Accuracy 1: ' + str((base.HAPLOTYPE_LENGTH - base.calculate_hamming_distance(
        best_sequence_pair['first'], haplotypes[0])) / base.HAPLOTYPE_LENGTH))
    print('Accuracy 2: ' + str((base.HAPLOTYPE_LENGTH - base.calculate_hamming_distance(
        best_sequence_pair['second'], haplotypes[1])) / base.HAPLOTYPE_LENGTH))


def start():
    experience_number = base.get_experience_number()
    if experience_number == 'all':
        for i in range(base.ALL_EXPERIENCES_COUNT):
            search(i)
    else:
        search(experience_number)
    base.print_results(experience_number == 'all', FRAGMENTS_COUNT)


start()
