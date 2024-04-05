import sys
import json
import argparse

# (n+4)-bit binary string
def calculate_ancilla(histogram, n, bit):
    # bit = 0 -> MSB
    # bit = 1 -> 2nd MSB
    # bit = 3 -> 3rd MSB

    total_prob = 0

    # loop through each key-value pair in the histogram
    for key, value in histogram.items():
        key_int = int(key)
        bit_index = n + 3 - bit

        # the mask for the current bit
        mask = 1 << bit_index

        if mask & key_int:  # if the bit at bit_index is 1
            total_prob += value

    return round(total_prob, 4)


parser = argparse.ArgumentParser(description='Calculate ancilla probabilities.')
parser.add_argument('--n', type=int, help='The line number', required=True)
parser.add_argument('--name', type=str, help='Input name', required=True)
args = parser.parse_args()

# Read the histogram JSON from stdin
histogram_json = sys.stdin.readline()
histogram = json.loads(histogram_json)

n = args.n
ancillas = []
for i in range(n):
    prob = calculate_ancilla(histogram, n, i)
    ancillas.append(prob)

ancillas.reverse()
print(' '.join(str(prob) for prob in ancillas))
