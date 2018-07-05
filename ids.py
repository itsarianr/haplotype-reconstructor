import time
import sys

DATA_DIRECTORY = 'data/'
HAPLOTYPE_LENGTH = 100
EXPERIENCES_COUNT = 100


def get_experience_number():
    try:
        return sys.argv[1]
    except:
        raise 'Please enter experience number!'


def read_data_from_file(experience_number, type):
    file_name = '%sexp%s.%ss' % (DATA_DIRECTORY, experience_number, type)
    with open(file_name) as file:
        return [line.rstrip('\n') for line in file]


def generate_base_reference_sequence():
    return '-' * HAPLOTYPE_LENGTH


def are_compatible(reference_sequence, fragment):
    return calculate_hamming_distance(reference_sequence, fragment) == 0


def calculate_hamming_distance(v1, v2):
    hamming_distance = 0
    for i in range(0, len(v1)):
        if v1[i] != '-' and v2[i] != '-' and v1[i] != v2[i]:
            hamming_distance += 1
    return hamming_distance


def combine(reference_sequence, fragment):
    reference_sequence_list = list(reference_sequence)
    for index, nucleotide in enumerate(reference_sequence_list):
        if nucleotide == '-':
            reference_sequence_list[index] = fragment[index]
    return ''.join(reference_sequence_list)


def search(experience_number):
    fragments = read_data_from_file(experience_number, 'fragment')
    first_reference_sequence = generate_base_reference_sequence()
    second_reference_sequence = generate_base_reference_sequence()
    for fragment in fragments:
        if are_compatible(first_reference_sequence, fragment):
            first_reference_sequence = combine(
                first_reference_sequence, fragment)
        elif are_compatible(second_reference_sequence, fragment):
            second_reference_sequence = combine(
                second_reference_sequence, fragment)
        else:
            print('WTF?!')
    haplotypes = read_data_from_file(experience_number, 'haplotype')
    if (are_compatible(haplotypes[0], first_reference_sequence)
            and are_compatible(haplotypes[1], second_reference_sequence)):
        print('100% match!')
    print('-----')


def start():
    experience_number = get_experience_number()
    if experience_number == 'all':
        for i in range(EXPERIENCES_COUNT):
            search(i)
    else:
        search(experience_number)


start_time = time.clock()
start()
print('- Duration: ' + str((time.clock() - start_time) * 1000) + ' milliseconds.')
