import sys
import json
import matplotlib.pyplot as plt


def sort_key(string):
    # Convert number string to integer for sorting purposes
    return int(string)


# read the histogram data from stdin
histogram_no_noise = json.loads(sys.argv[1])
histogram_noisy = json.loads(sys.argv[2])

# no noise simulation outcome
outcomes1 = list(histogram_no_noise.keys())

# noisy simulation outcome
outcomes2 = list(histogram_noisy.keys())

# merge and sort outcomes
outcomes = list(set(outcomes1 + outcomes2))
outcomes.sort(key=sort_key)

# match the prob with sorted outcome
probabilities1 = [histogram_no_noise.get(outcome, 0) for outcome in outcomes]
probabilities2 = [histogram_noisy.get(outcome, 0) for outcome in outcomes]


# plot
plt.figure(figsize=(10, 6))

bar_width = 0.35

plt.bar([i - bar_width/2 for i in range(len(outcomes))], probabilities1, width=bar_width, label='ideal simulator',
        align='center', alpha=0.7, color='skyblue')

plt.bar([i + bar_width/2 for i in range(len(outcomes))], probabilities2, width=bar_width, label='noisy simulator',
        align='center', alpha=0.7,  color='red')

plt.xlabel('Output state')
plt.ylabel('Probability')
plt.title('2-layer 2 ancilla ')
plt.xticks(range(len(outcomes)), outcomes, rotation=90)
plt.legend()

plt.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
plt.savefig('result_new1.png')
print("plot saved as result_new1.png")

#key = IgkFjo6qRSSFOpo7bZkexODWXadlQIMl