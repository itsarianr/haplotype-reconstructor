import base
import random

FRAGMENTS_COUNT = 0
MAX_WORSE_NEIGHBOUR_CHECK_COUNT = 10
MAX_HILL_CLIMBS_COUNT = 10


def increase_fragments_count(fragments):
    global FRAGMENTS_COUNT
    FRAGMENTS_COUNT += len(fragments)


def climb_hill(fragments):
    worse_neighbour_check_count = 0
    first_reference_sequence = base.generate_random_reference_sequence()
    second_reference_sequence = base.generate_random_reference_sequence()
    total_score = base.calculate_total_reference_sequences_fitness_score(
        first_reference_sequence, second_reference_sequence, fragments)
    while True:
        first_random_neighbour = base.get_random_neighbour(
            first_reference_sequence)
        second_random_neighbour = base.get_random_neighbour(
            second_reference_sequence)
        neighbour_total_score = base.calculate_total_reference_sequences_fitness_score(
            first_random_neighbour, second_random_neighbour, fragments)
        if neighbour_total_score > total_score:
            print('better...')
            first_reference_sequence = first_random_neighbour
            second_reference_sequence = second_random_neighbour
        else:
            print('worse...')
            if worse_neighbour_check_count >= MAX_WORSE_NEIGHBOUR_CHECK_COUNT:
                return {
                    'first': first_reference_sequence,
                    'second': second_reference_sequence,
                    'score': total_score
                }
            worse_neighbour_check_count += 1


def search(experience_number):
    fragments = base.read_data_from_file(experience_number, 'fragment')
    increase_fragments_count(fragments)
    best_reference_seq = {
        'first': None,
        'second': None,
        'score': 0
    }
    for i in range(MAX_HILL_CLIMBS_COUNT):
        print('hill climb number ' + str(i) + '...')
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
