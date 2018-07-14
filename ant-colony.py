import base
import itertools
import random
import math
import pprint

FRAGMENTS_COUNT = 0
ANTS_COUNT = 10
EDGES_PHEROMONES = []
PHEREMONE_EVAPORATION_RATE = 0.01


def increase_fragments_count(fragments):
    global FRAGMENTS_COUNT
    FRAGMENTS_COUNT += len(fragments)


def generate_base_sequence():
    return '-' * base.HAPLOTYPE_LENGTH


def are_compatible(sequence1, sequence2):
    return base.calculate_hamming_distance(sequence1, sequence2) == 0


def combine_sequence(sequence, fragment):
    sequence_list = list(sequence)
    for index, nucleotide in enumerate(sequence_list):
        if nucleotide == '-':
            sequence_list[index] = fragment[index]
    return ''.join(sequence_list)


def init_edges_pheromones(fragments_count):
    for i in range(len(fragments_count)):
        EDGES_PHEROMONES.append({'edge': (-1, i), 'pheromone': 1})
    for item in itertools.combinations(range(len(fragments_count)), 2):
        EDGES_PHEROMONES.append({'edge': item, 'pheromone': 1})


def search_edges_pheromones(fragments_path):
    last_fragment = fragments_path[-1]
    elements = [x for x in EDGES_PHEROMONES if last_fragment in x['edge']]
    new_elements = []
    for element in elements:
        if element['edge'][0] == last_fragment and (not element['edge'][1] in fragments_path):
            new_elements.append(element)
        if element['edge'][1] == last_fragment and (not element['edge'][0] in fragments_path):
            new_elements.append(element)
    return new_elements


def calculate_edges_probabilities(elements):
    probabilities = []
    pheromone_sum = 0
    for element in elements:
        pheromone_sum += element['pheromone']
    for element in elements:
        probability = element['pheromone'] / pheromone_sum
        probabilities.append(probability)
    return probabilities


def get_next_fragment(fragments, fragments_path):
    elements = search_edges_pheromones(fragments_path)
    probabilities = calculate_edges_probabilities(elements)
    element = random.choices(elements, weights=probabilities)[0]
    if element['edge'][0] == fragments_path[-1]:
        return fragments[element['edge'][1]]
    else:
        return fragments[element['edge'][0]]


def calculate_sequences_score(sequences, fragments):
    return 50 * base.calculate_total_reference_sequences_fitness_score(
        sequences['first'], sequences['second'], fragments)


def update_pheromones(path, score):
    each_score = score / len(path)
    path_elements = []
    for i in range(len(path)):
        if i + 2 == len(path):
            break
        edge = ()
        if path[i + 1] > path[i]:
            edge = (path[i], path[i + 1])
        else:
            edge = (path[i + 1], path[i])
        path_elements.append(
            next(x for x in EDGES_PHEROMONES if x['edge'] == edge))
    for element in EDGES_PHEROMONES:
        delta_pheremone = 0
        if element in path_elements:
            delta_pheremone = each_score
        element['pheromone'] = (1 - PHEREMONE_EVAPORATION_RATE) * \
            element['pheromone'] + delta_pheremone
    # pprint.pprint(EDGES_PHEROMONES)


def deploy_ant(fragments):
    sequences = {
        'first': generate_base_sequence(),
        'second': generate_base_sequence(),
        'score': 0
    }
    path_so_far = [-1]
    while True:
        if len(path_so_far) == len(fragments):
            break
        fragment = get_next_fragment(fragments, path_so_far)
        if are_compatible(sequences['first'], fragment):
            sequences['first'] = combine_sequence(
                sequences['first'], fragment)
            path_so_far.append(fragments.index(fragment))
        elif are_compatible(sequences['second'], fragment):
            sequences['second'] = combine_sequence(
                sequences['second'], fragment)
            path_so_far.append(fragments.index(fragment))
        else:
            break
    sequences['score'] = calculate_sequences_score(sequences, fragments)
    update_pheromones(path_so_far, sequences['score'])
    return sequences


def search(experience_number):
    fragments = base.read_data_from_file(experience_number, 'fragment')
    increase_fragments_count(fragments)
    init_edges_pheromones(fragments)
    best_sequences = {
        'score': 0
    }
    for i in range(ANTS_COUNT):
        print('Deploying ant number ' + str(i) + '...')
        sequences = deploy_ant(fragments)
        if sequences['score'] > best_sequences['score']:
            best_sequences['first'] = sequences['first']
            best_sequences['second'] = sequences['second']
            best_sequences['score'] = sequences['score']
    haplotypes = base.read_data_from_file(experience_number, 'haplotype')
    print('Accuracy 1: ' + str((base.HAPLOTYPE_LENGTH - base.calculate_hamming_distance(
        best_sequences['first'], haplotypes[0])) / base.HAPLOTYPE_LENGTH))
    print('Accuracy 2: ' + str((base.HAPLOTYPE_LENGTH - base.calculate_hamming_distance(
        best_sequences['second'], haplotypes[1])) / base.HAPLOTYPE_LENGTH))


def start():
    experience_number = base.get_experience_number()
    if experience_number == 'all':
        for i in range(base.ALL_EXPERIENCES_COUNT):
            search(i)
    else:
        search(experience_number)
    base.print_results(experience_number == 'all', FRAGMENTS_COUNT)


start()
