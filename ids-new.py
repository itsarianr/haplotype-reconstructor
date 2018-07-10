import base
import traceback

FRAGMENTS_COUNT = 0


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


def combine(sequences, fragment):
    if are_compatible(sequences['first'], fragment):
        sequences['first'] = combine_sequence(sequences['first'], fragment)
    elif are_compatible(sequences['second'], fragment):
        sequences['second'] = combine_sequence(sequences['second'], fragment)
    else:
        first_hd = base.calculate_hamming_distance(
            sequences['first'], fragment)
        second_hd = base.calculate_hamming_distance(
            sequences['second'], fragment)
        if first_hd < second_hd:
            sequences['first'] = combine_sequence(sequences['first'], fragment)
        else:
            sequences['second'] = combine_sequence(
                sequences['second'], fragment)
    return sequences


def test_goal(sequences, fragments):
    for i in range(len(sequences['first'])):
        if sequences['first'][i] == '-' or sequences['second'][i] == '-':
            return False
    for fragment in fragments:
        if not are_compatible(sequences['first'], fragment) and not are_compatible(sequences['second'], fragment):
            return False
    return True


def recursive_depth_limited_search(sequences, fragments, limit):
    if test_goal(sequences, fragments):
        return sequences
    elif limit == 0:
        raise Exception('Cutoff!')
    for fragment in fragments:
        fragments_copy = fragments.copy()
        fragments_copy.remove(fragment)
        return recursive_depth_limited_search(
            combine(sequences, fragment), fragments_copy, limit - 1)
    raise Exception('Failure!')


def depth_limited_search(depth, fragments):
    initial_sequences = {
        'first': generate_base_sequence(),
        'second': generate_base_sequence()
    }
    return recursive_depth_limited_search(initial_sequences, fragments, depth)


def iterative_deepening_search(fragments):
    for depth in range(len(fragments)):
        depth += 1
        print('Searching in depth ' + str(depth) + '...')
        try:
            result = depth_limited_search(depth, fragments)
            print('Result ' + str(result) +
                  ', Found in depth ' + str(depth) + '.')
            return result
        except Exception as e:
            if str(e) == 'Cutoff!':
                print('Cutoff!')
                continue
            elif str(e) == 'Failure!':
                print('Not found :(')
                raise e
            else:
                print('Unkown error.')
                traceback.print_exc()
                raise e
    print('Technicaly we should never get here...')


def search(experience_number):
    fragments = base.read_data_from_file(experience_number, 'fragment')
    increase_fragments_count(fragments)
    result = iterative_deepening_search(fragments)
    haplotypes = base.read_data_from_file(experience_number, 'haplotype')
    print('Accuracy 1: ' + str((base.HAPLOTYPE_LENGTH - base.calculate_hamming_distance(
        result['first'], haplotypes[0])) / base.HAPLOTYPE_LENGTH))
    print('Accuracy 2: ' + str((base.HAPLOTYPE_LENGTH - base.calculate_hamming_distance(
        result['second'], haplotypes[1])) / base.HAPLOTYPE_LENGTH))


def start():
    experience_number = base.get_experience_number()
    search(experience_number)
    base.print_results(False, FRAGMENTS_COUNT)


start()
