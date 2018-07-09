import base

FRAGMENTS_COUNT = 0


def generate_base_reference_sequence():
    return '-' * base.HAPLOTYPE_LENGTH


def are_compatible(reference_sequence, fragment):
    return base.calculate_hamming_distance(reference_sequence, fragment) == 0


def combine(reference_sequence, fragment):
    reference_sequence_list = list(reference_sequence)
    for index, nucleotide in enumerate(reference_sequence_list):
        if nucleotide == '-':
            reference_sequence_list[index] = fragment[index]
    return ''.join(reference_sequence_list)


def search(experience_number):
    global FRAGMENTS_COUNT
    fragments = base.read_data_from_file(experience_number, 'fragment')
    FRAGMENTS_COUNT += len(fragments)
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
            print('Conflict.')
    haplotypes = base.read_data_from_file(experience_number, 'haplotype')
    if (are_compatible(haplotypes[0], first_reference_sequence)
            and are_compatible(haplotypes[1], second_reference_sequence)):
        print('100% match!')


def start():
    experience_number = base.get_experience_number()
    if experience_number == 'all':
        for i in range(base.ALL_EXPERIENCES_COUNT):
            search(i)
    else:
        search(experience_number)
    base.print_results(experience_number == 'all', FRAGMENTS_COUNT)


start()
