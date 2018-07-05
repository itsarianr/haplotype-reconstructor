import time

NUCLEOTIDES = ['A', 'T', 'G', 'C']
SEQUENCES_LENGTH = 8

FRAGMENT_SEQUENCES = [
    'A-TA--TT',
    '-TT-C-T-',
    'A--A-C-T',
    # 'GA-CG-AT',
    # '---C-GA-',
    # '-AT-GG--'
]


def iterative_deepening_search():
    for depth in range(SEQUENCES_LENGTH):
        depth += 1
        print('Searching in depth ' + str(depth) + '...')
        result = depth_limited_search(depth)
        if result:
            print('Result ' + result + ', Found in depth ' + str(depth) + '.')
            return
    print('Not found :(')


def depth_limited_search(depth):
    reference_sequences = generate_reference_sequences_by_length(depth)
    for reference_sequence in reference_sequences:
        is_all_equal = True
        for fragment_sequence in FRAGMENT_SEQUENCES:
            is_all_equal = is_all_equal and is_equal(
                normalize_sequence(reference_sequence), fragment_sequence)
        if is_all_equal:
            return reference_sequence
    return None


def generate_reference_sequences_by_length(length,
                                           generated_reference_sequences=NUCLEOTIDES):
    if length == 1:
        return generated_reference_sequences
    next_generated_reference_sequences = []
    for nucleotide in NUCLEOTIDES:
        for reference_sequence in generated_reference_sequences:
            reference_sequence += nucleotide
            next_generated_reference_sequences.append(reference_sequence)
    return generate_reference_sequences_by_length(
        length - 1, next_generated_reference_sequences)


def is_equal(reference_sequence, fragment_sequence):
    return calculate_hamming_distance(reference_sequence, fragment_sequence) == 0


def calculate_hamming_distance(v1, v2):
    hamming_distance = 0
    for i in range(0, len(v1)):
        if v2[i] != '-' and v1[i] != v2[i]:
            hamming_distance += 1
    return hamming_distance


def normalize_sequence(sequence):
    normalized_sequence = ''
    for i in range(SEQUENCES_LENGTH):
        try:
            normalized_sequence += sequence[i]
        except:
            normalized_sequence += '?'
    return normalized_sequence


start_time = time.clock()
iterative_deepening_search()
print('- Duration: ' + str(time.clock() - start_time) + ' seconds.')
