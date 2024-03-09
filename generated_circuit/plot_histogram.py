import sys
import json
import matplotlib.pyplot as plt

# read the JSON array of probabilities from the command line
probabilities_of_0 = json.loads(sys.argv[1])

# convert from string to float
probabilities_of_0 = [float(prob) for prob in probabilities_of_0]

#probabilities_of_0 = [0.96484, 0.90332, 0.88574, 0.85254, 0.81738, 0.76758, 0.72949, 0.698242, 0.671875, 0.649414]

print(probabilities_of_0)

n = len(probabilities_of_0)

plt.figure(figsize=(12, 6))

plt.plot(range(1, n+1), probabilities_of_0, marker='o', color='blue', linestyle='-', linewidth=2, markersize=6)

plt.xlabel('N = ')
plt.ylabel('Probability of "0"')
plt.title(f'P(0) for {n}-depth 4-cnot (type a) Forte-simulator')
plt.xticks(range(1, n+1))
plt.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5, alpha=0.7)

plt.tight_layout()
plt.savefig('result3.png')
print("Result saved as result3.png")
