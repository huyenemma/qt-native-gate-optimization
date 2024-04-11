import sys
import json


def calculate_probability_ancilla(histogram):
    prob_a = sum(value for key, value in histogram.items() if 0 <= int(key) <= 15)
    return 1 - prob_a


def calculate_ancilla(histogram):
    # bit = 0 -> MSB
    # bit = 1 -> 2nd MSB
    # bit = 3 -> 3rd MSB

    total_prob = 0

    # loop through each key-value pair in the histogram
    for key, value in histogram.items():
        key_int = int(key)
        bit_index = 4

        # the mask for the current bit
        mask = 1 << bit_index

        if mask & key_int:  # if the bit at bit_index is 1
            total_prob += value

    return round(total_prob, 4)


# Read the histogram JSON from stdin
histogram_json = sys.stdin.readline()
histogram = json.loads(histogram_json)

# Calculate the probability
prob_a = calculate_ancilla(histogram)
print(prob_a)


