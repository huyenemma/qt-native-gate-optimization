import sys
import json


def calculate_probability_ancilla(histogram):
    prob_a = sum(value for key, value in histogram.items() if 0 <= int(key) <= 15)
    return prob_a


# Read the histogram JSON from stdin
histogram_json = sys.stdin.readline()
histogram = json.loads(histogram_json)

# Calculate the probability
prob_a = round(calculate_probability_ancilla(histogram), 3)
print(prob_a)
