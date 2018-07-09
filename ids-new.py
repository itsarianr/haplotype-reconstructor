import base

FRAGMENTS_COUNT = 0


def increase_fragments_count(fragments):
    global FRAGMENTS_COUNT
    FRAGMENTS_COUNT += len(fragments)


def generate_base_sequence():
    return '-' * base.HAPLOTYPE_LENGTH


def are_compatible(sequence1, sequence2):
    return base.calculate_hamming_distance(sequence1, sequence2) == 0


def combine(sequence, fragment):
    sequence_list = list(sequence)
    for index, nucleotide in enumerate(sequence_list):
        if nucleotide == '-':
            sequence_list[index] = fragment[index]
    return ''.join(sequence_list)


def depth_limited_search(depth, fragments):
    first_sequence = generate_base_sequence()
    second_sequence = generate_base_sequence()
    for fragment in fragments:
        if are_compatible(first_sequence, fragment):
            combine(first_sequence, fragment)
        elif are_compatible(second_sequence, fragment):
            combine(second_sequence, fragment)
        # TODO WTF :(


def iterative_deepening_search(fragments):
    for depth in range(len(fragments)):
        depth += 1
        print('Searching in depth ' + str(depth) + '...')
        result = depth_limited_search(depth, fragments)
        result = None
        if result:
            print('Result ' + result + ', Found in depth ' + str(depth) + '.')
            return
    print('Not found :(')


def search(experience_number):
    fragments = base.read_data_from_file(experience_number, 'fragment')
    increase_fragments_count(fragments)
    iterative_deepening_search(fragments)


def start():
    experience_number = base.get_experience_number()
    search(experience_number)
    base.print_results(False, FRAGMENTS_COUNT)


start()
