
from qiskit import QuantumCircuit
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils import run_circuit


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
        key_int = int(key)
        bit_index = n + 3 - bit

        # the mask for the current bit
        mask = 1 << bit_index

        if mask & key_int:  # if the bit at bit_index is 1
            total_count += value

    return round(total_count, 4)


def get_ancilla_probabilities(iters, shots, backend, optimization_level=0):
    results = []
    for n in range(1,iters+1):
        probs = []
        circuit = generate_circuit(n)
        histogram = run_circuit(circuit,
                                shots, 
                                backend=backend, 
                                optimization_level=optimization_level)
        for i in range(n): 
            probability = calculate_ancilla(histogram, n, n-i)
            probs.append(probability)
        results.append(probs)
        
    return results

def create_df(results):
    df = pd.DataFrame(results)
    df = df.fillna(0)
    df.index = range(1,len(df)+1)
    df.columns = range(1, len(df.columns) + 1)
    return df

def plot_heatmap(results, optimization_level): 
    plt.figure(figsize=(10, 8))
    df = create_df(results)
    vmax = df.values.max()
    sns.heatmap(df, annot=True, cmap='coolwarm', vmin=0, vmax=vmax)
    #plt.title(f'P(ancilla)=1, opt_level={optimization_level}') 
    plt.xlabel('Ancilla Qubits')
    plt.ylabel('N (number of repetitions)')
    plt.savefig(f'fresh.png')
    plt.show()
    
def plag_error_rate(results, n): 
    
    error_rate = 0
    # for i in range(2, n+1):
    #     error_rate += results[i-1][i-1] - results[i-2][i-2]
    
    error_rate = results[n-1][n-1] - results[0][0]
    result = error_rate/((n-1)/2)
    
    return round(result, 4)