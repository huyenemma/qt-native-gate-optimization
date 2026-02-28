from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
import pandas as pd


def create_df(data_string):
    # Split the string into lines
    lines = data_string.strip().split('\n')

    # Convert each line to a list and store in a 2D array
    array_2d = [line.split('\t') for line in lines]

    for i in range(len(array_2d)):
        array_2d[i] = [float(x) if x else None for x in array_2d[i]]

    # Convert the data to a DataFrame
    df = pd.DataFrame(array_2d)
    # Assuming the missing values are meant to be zeros
    df = df.fillna(0)

    df.index = range(0, len(df)) 
    df.columns = range(0, len(df.columns))

    return df


def run_circuit(circuit:QuantumCircuit, shots, backend, optimization_level=0):

    pm = generate_preset_pass_manager(optimization_level=optimization_level, backend=backend)
    compiled_qc = pm.run(circuit)
    print(backend.name)
    if backend.name.startswith("fake_"):
        
        job = backend.run(compiled_qc, shots=shots)
        result = job.result()
        histogram = result.get_counts(compiled_qc)    
    else: 
        sampler = Sampler(mode=backend)
        
        job = sampler.run([compiled_qc], shots=shots)
        result = job.result()[0]
        histogram = result.data.meas.get_counts()
    #print(histogram)
    #histogram = result.get_counts(qc)
    histogram = {key: value/shots for key, value in histogram.items()}
    return histogram
