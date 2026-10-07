from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from utils import run_circuit, plaquette_layout

def generate_circuit(n):
    repeat_block = QuantumCircuit(5)
    repeat_block.cx(4,3)
    repeat_block.cx(4,2)
    repeat_block.cx(4,1)
    repeat_block.cx(4,0)
    repeat_block.barrier()

    qc = QuantumCircuit(5)
    for _ in range(n): 
        qc.compose(repeat_block, inplace=True)
    qc.measure_all()
    return qc


def calculate_ancilla(histogram):
    total_prob = 0

    # loop through each key-value pair in the histogram
    for key, value in histogram.items():
        key_int = int(key, 2)
        bit_index = 4

        # the mask for the current bit
        mask = 1 << bit_index

        if mask & key_int:  # if the bit at bit_index is 1
            total_prob += value

    return round(total_prob, 4)


def get_ancilla_probabilities(iters, shots, backend, optimization_level=0, save_dir=None, data_qubits=None,
                              seed_transpiler=None):
    results = []
    for n in range(1,iters+1):
        circuit = generate_circuit(n)
        histogram = run_circuit(circuit, 
                                shots, 
                                backend=backend, 
                                optimization_level=optimization_level,
                                seed_transpiler=seed_transpiler,
                                initial_layout=plaquette_layout(backend, data_qubits, 1),
                                save_path=save_dir and f"{save_dir}/recycle_opt{optimization_level}_n{n}.json")
        probability = calculate_ancilla(histogram)
        results.append(probability)
        
    return results

def plot(results): 
    plt.figure(figsize=(10, 8))
    plt.plot(range(1, len(results)+1), results, marker='o')
    plt.title('P(ancilla=1)')
    plt.xlabel('N (number of repetitions)')
    plt.ylabel('P(1)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def plot_all_results(results0, results1, results2, n):
    x = range(1, n + 1)

    plt.figure(figsize=(10, 8))

    plt.plot(x, results0[:n], label="opt_level=0")
    plt.plot(x, results1[:n], label="opt_level=1")
    plt.plot(x, results2[:n], label="opt_level=2")

    #plt.title("P(ancilla=1)")
    plt.xlabel("N (number of repetitions)")
    plt.ylabel("P(ancilla=1)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def corr_err(fresh, recycle, n):
    # Eq. (4): corre = 1/(n-1) * sum_{i=2}^{n} (p_i - p_ii) / (i-1)
    corr = 0.0
    for i in range(2, n + 1):
        corr += (recycle[i-1] - fresh[i-1][i-1]) / (i - 1)
    return corr / (n - 1)


def plag_error_rate(avg_corr, results, n):
    # Eq. (7)-(8): plaq_R = 1/(n-1) * sum_{i=2}^{n} (p_i - p_(i-1) - corre)
    #                     = (p_n - p_1) / (n-1) - corre
    error_rate = (results[n-1] - results[0]) / (n - 1) - avg_corr

    return round(error_rate, 4)
