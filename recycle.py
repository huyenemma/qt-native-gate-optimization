from qiskit import QuantumCircuit
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator

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
        key_int = int(key)
        bit_index = 4

        # the mask for the current bit
        mask = 1 << bit_index

        if mask & key_int:  # if the bit at bit_index is 1
            total_prob += value

    return round(total_prob, 4)


def run_circuit(n, shots, backend, optimization_level=0):
    qc = generate_circuit(n)
    
    pm = generate_preset_pass_manager(optimization_level=optimization_level, backend=backend)
    compiled_qc = pm.run(qc)
    
    estimator = Estimator(mode=backend)
    job = backend.run(compiled_qc, shots=shots)
    result = job.result()
    histogram = result.get_counts(qc)
    histogram = {key: value/shots for key, value in histogram.items()}
    return histogram

def get_ancilla_probabilities(iters, shots, backend, optimization_level=0):
    results = []
    for n in range(1,iters+1):
        histogram = run_circuit(n, shots, backend=backend, optimization_level=optimization_level)
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
    
def corr_err(fresh, recycle, n):
    corr = 0.0
    for i in range(2, n + 1): 
        corr += (recycle[i-1] - fresh[i-1][i-1]) / ((i - 1) ** 2)
        print(corr)
    return corr / n


def plag_error_rate(avg_corr, results, n):
    error_rate = 0.0
    # for i in range(2, n + 1):  
    #     print(results[i-1], results[i-2], avg_corr)
    #     error_rate += results[i-1] - results[i-2] - avg_corr
    error_rate = results[-1] - results[0] - avg_corr * (n - 1)

    return round(error_rate / n, 4)