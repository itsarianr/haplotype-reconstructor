import time
import sys

DATA_DIRECTORY = 'data/'
ALL_EXPERIENCES_COUNT = 100
HAPLOTYPE_LENGTH = 100
START_TIME = 0


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
