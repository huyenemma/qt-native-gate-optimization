import sys
import json
import matplotlib.pyplot as plt

# read the JSON array of probabilities from the command line
probabilities_of_0 = json.loads(sys.argv[1])

# convert from string to float
probabilities_of_0 = [float(prob) if prob is not None else 0.0 for prob in probabilities_of_0]

print(probabilities_of_0)

n = len(probabilities_of_0)

plt.figure(figsize=(12, 6))

plt.plot(range(1, n+1), probabilities_of_0, marker='o', color='blue', linestyle='-', linewidth=2, markersize=6)

plt.xlabel('N = ')
plt.ylabel('Probability of "0"')
plt.title(f'P(0) for {n}-depth 4-cnot (type a) Aria1')
plt.xticks(range(1, n+1))
plt.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.7)

plt.tight_layout()
plt.savefig('result2.png')
print("Result saved as result2.png")
