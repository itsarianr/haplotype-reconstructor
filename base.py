import time
import sys
import random
import math

DATA_DIRECTORY = 'data/'
ALL_EXPERIENCES_COUNT = 100
HAPLOTYPE_LENGTH = 100
START_TIME = 0
NUCLEOTIDES = ['a', 't', 'g', 'c']


def get_experience_number():
    global START_TIME
    START_TIME = time.clock()
    try:
        return sys.argv[1]
    except:
        raise 'Please enter experience number!'


def read_data_from_file(experience_number, type):
    file_name = '%sexp%s.%ss' % (DATA_DIRECTORY, experience_number, type)
    with open(file_name) as file:
        return [line.rstrip('\n') for line in file]


def print_results(did_run_on_all_experiences, fragments_count):
    experience_count = ALL_EXPERIENCES_COUNT if did_run_on_all_experiences else 1
    print('\033[92mReconstructed ' + str(experience_count * 2) +
          ' haplotypes using ' + str(fragments_count) + ' fragments in ' +
          str((time.clock() - START_TIME) * 1000) + ' milliseconds. \033[0m')


def calculate_hamming_distance(v1, v2):
    hamming_distance = 0
    for i in range(0, len(v1)):
        if v1[i] != '-' and v2[i] != '-' and v1[i] != v2[i]:
            hamming_distance += 1
    return hamming_distance


def generate_random_reference_sequence():
    reference_sequence = []
    for i in range(HAPLOTYPE_LENGTH):
        reference_sequence.append(random.choice(NUCLEOTIDES))
    return ''.join(reference_sequence)


def calculate_reference_sequences_hamming_distance(first_reference_sequence,
                                                   second_reference_sequence,
                                                   fragment):
    first_hamming_distance = calculate_hamming_distance(
        first_reference_sequence, fragment)
    second_hamming_distance = calculate_hamming_distance(
        second_reference_sequence, fragment)
    return min(first_hamming_distance, second_hamming_distance)


def calculate_total_reference_sequences_fitness_score(first_reference_sequence,
                                                      second_reference_sequence,
                                                      fragments):
    reference_sequences_total_hamming_distance = 0
    for fragment in fragments:
        reference_sequences_total_hamming_distance += calculate_reference_sequences_hamming_distance(
            first_reference_sequence, first_reference_sequence, fragment)
    if reference_sequences_total_hamming_distance == 0:
        return math.inf
    return 1 / reference_sequences_total_hamming_distance


def get_random_neighbour(reference_sequence):
    random_index = random.randint(0, HAPLOTYPE_LENGTH - 1)
    neighbour_reference_sequence = []
    for index, nucleotide in enumerate(reference_sequence):
        if index == random_index:
            valid_nucleotides = NUCLEOTIDES.copy()
            try:
                valid_nucleotides.remove(nucleotide)
            except:
                print('nucleotide:',nucleotide)
                raise 'ayy'
            neighbour_reference_sequence.append(
                random.choice(valid_nucleotides))
        else:
            neighbour_reference_sequence.append(nucleotide)
    return ''.join(neighbour_reference_sequence)
