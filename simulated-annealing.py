import base
import random
import math

FRAGMENTS_COUNT = 0
MAX_HILL_CLIMBS_COUNT = 1
MAX_TEMPERATURE = 100


def calculate_reference_sequences_hamming_distance(first_reference_sequence,
                                                   second_reference_sequence,
                                                   fragment):
    first_hamming_distance = base.calculate_hamming_distance(
        first_reference_sequence, fragment)
    second_hamming_distance = base.calculate_hamming_distance(
        second_reference_sequence, fragment)
    return min(first_hamming_distance, second_hamming_distance)


def calculate_total_reference_sequences_fitness_score(first_reference_sequence,
                                                      second_reference_sequence,
                                                      fragments):
    reference_sequences_total_hamming_distance = 0
    for fragment in fragments:
        reference_sequences_total_hamming_distance += calculate_reference_sequences_hamming_distance(
            first_reference_sequence, first_reference_sequence, fragment)
    return 1 / reference_sequences_total_hamming_distance


def get_random_neighbour(reference_sequence):
    random_index = random.randint(0, base.HAPLOTYPE_LENGTH - 1)
    neighbour_reference_sequence = []
    for index, nucleotide in enumerate(reference_sequence):
        if index == random_index:
            valid_nucleotides = base.NUCLEOTIDES.copy()
            valid_nucleotides.remove(nucleotide)
            neighbour_reference_sequence.append(
                random.choice(valid_nucleotides))
        else:
            neighbour_reference_sequence.append(nucleotide)
    return ''.join(neighbour_reference_sequence)


def increase_fragments_count(fragments):
    global FRAGMENTS_COUNT
    FRAGMENTS_COUNT += len(fragments)


def climb_hill(fragments):
    temperature = MAX_TEMPERATURE
    first_reference_sequence = base.generate_random_reference_sequence()
    second_reference_sequence = base.generate_random_reference_sequence()
    total_score = calculate_total_reference_sequences_fitness_score(
        first_reference_sequence, second_reference_sequence, fragments)
    while True:
        print(temperature)
        if temperature == 0:
            return {
                'first': first_reference_sequence,
                'second': second_reference_sequence,
                'score': total_score
            }
        first_random_neighbour = get_random_neighbour(
            first_reference_sequence)
        second_random_neighbour = get_random_neighbour(
            second_reference_sequence)
        neighbour_total_score = calculate_total_reference_sequences_fitness_score(
            first_random_neighbour, second_random_neighbour, fragments)
        if neighbour_total_score > total_score:
            print('better...')
            first_reference_sequence = first_random_neighbour
            second_reference_sequence = second_random_neighbour
        else:
            print('worse...')
            x = (total_score - neighbour_total_score) / temperature
            probability = math.exp(x)
            if random.random() <= probability:
                first_reference_sequence = first_random_neighbour
                second_reference_sequence = second_random_neighbour
        temperature -= 1


def search(experience_number):
    fragments = base.read_data_from_file(experience_number, 'fragment')
    increase_fragments_count(fragments)
    best_reference_seq = {
        'first': None,
        'second': None,
        'score': 0
    }
    for i in range(MAX_HILL_CLIMBS_COUNT):
        local_best_reference_seqs = climb_hill(fragments)
        if local_best_reference_seqs['score'] > best_reference_seq['score']:
            best_reference_seq = local_best_reference_seqs
    haplotypes = base.read_data_from_file(experience_number, 'haplotype')
    print('Accuracy 1: ' + str((base.HAPLOTYPE_LENGTH - base.calculate_hamming_distance(
        best_reference_seq['first'], haplotypes[0])) / base.HAPLOTYPE_LENGTH))
    print('Accuracy 2: ' + str((base.HAPLOTYPE_LENGTH - base.calculate_hamming_distance(
        best_reference_seq['second'], haplotypes[1])) / base.HAPLOTYPE_LENGTH))


def start():
    experience_number = base.get_experience_number()
    if experience_number == 'all':
        for i in range(base.ALL_EXPERIENCES_COUNT):
            search(i)
    else:
        search(experience_number)
    base.print_results(experience_number == 'all', FRAGMENTS_COUNT)


start()
