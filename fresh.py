
from qiskit import QuantumCircuit
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils import run_circuit, plaquette_layout


def generate_circuit(n:int):
    qc = QuantumCircuit(n+4)
    for i in range(4,n+4):
        qc.cx(i,3)
        qc.cx(i,2)
        qc.cx(i,1)
        qc.cx(i,0)
        qc.barrier()
    qc.measure_all()
    return qc


# (n+4)-bit binary string
def calculate_ancilla(histogram, n, bit):
    # the sum of the probabilities of all outcomes
    # where the bit at bit position is 1"

    total_count = 0

    # loop through each key-value pair in the histogram
    for key, value in histogram.items():
        key_int = int(key, 2)
        # qubits 0-3 are data, qubit 4 + (y-1) is the ancilla of the y-th plaquette
        bit_index = n + 4 - bit

        # the mask for the current bit
        mask = 1 << bit_index

        if mask & key_int:  # if the bit at bit_index is 1
            total_count += value

    return round(total_count, 4)


def get_ancilla_probabilities(iters, shots, backend, optimization_level=0, save_dir=None, data_qubits=None,
                              seed_transpiler=None):
    results = []
    for n in range(1,iters+1):
        probs = []
        circuit = generate_circuit(n)
        histogram = run_circuit(circuit,
                                shots, 
                                backend=backend, 
                                optimization_level=optimization_level,
                                seed_transpiler=seed_transpiler,
                                initial_layout=plaquette_layout(backend, data_qubits, n),
                                save_path=save_dir and f"{save_dir}/fresh_opt{optimization_level}_n{n}.json")
        for i in range(n): 
            probability = calculate_ancilla(histogram, n, n-i)
            probs.append(probability)
        results.append(probs)
        
    return results

def create_df(results):
    df = pd.DataFrame(results)
    #df = df.fillna(0)
    # utils.create_df tables carry their own 0-based index; plain lists are ordered n = 1..len
    df.index = df.index + 1 if isinstance(results, pd.DataFrame) else range(1, len(df) + 1)
    # largest n on top, as in the IBM / IonQ heatmaps
    df = df.sort_index(ascending=False)
    df.columns = range(1, len(df.columns) + 1)
    return df

def plot_heatmap(results, optimization_level): 
    plt.rcParams.update({'font.size': 20})
    plt.figure(figsize=(10, 8))
    df = create_df(results)
    vmax = 0.35 #df.values.max()
    sns.heatmap(df, annot=True, cmap='coolwarm', vmin=0, vmax=vmax)
    #plt.title(f'P(ancilla)=1, opt_level={optimization_level}') 
    plt.xlabel('Index of Ancilla Qubit',)
    plt.ylabel('No. of Repetitions (n)',)
    plt.savefig(f'fresh.png')
    plt.show()
    
def plag_error_rate(results, n, window=False):
    # results[x-1][x-1] = p_xx, works for nested lists and utils.create_df DataFrames
    p = lambda x: results[x-1][x-1]

    if window:
        # early-time estimator over 3-step windows, Eq. (12):
        # plaq_F = 1/(n-2) * sum_{i=1}^{n-2} (p_(i+2)(i+2) - p_ii) / 2
        error_rate = sum((p(i+2) - p(i)) / 2 for i in range(1, n-1)) / (n - 2)
    else:
        # Eq. (5)-(6): plaq_F = (p_nn - p_11) / (n-1)
        error_rate = (p(n) - p(1)) / (n - 1)

    return round(error_rate, 4)
