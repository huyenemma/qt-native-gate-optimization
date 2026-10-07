import json
import os
from datetime import datetime, timezone

from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler, IBMBackend
import pandas as pd


def create_df(data_string):
    # Split the string into lines
    lines = data_string.strip().split('\n')

    # Convert each line to a list and store in a 2D array
    array_2d = [line.split('\t') for line in lines]
    array_2d.reverse()

    for i in range(len(array_2d)):
        array_2d[i] = [float(x) if x else None for x in array_2d[i]]

    # Convert the data to a DataFrame
    df = pd.DataFrame(array_2d)
    # Assuming the missing values are meant to be zeros
    #df = df.fillna(0)

    df.index = [6,5,4,3,2,1,0]# range(0, len(df))
    df.columns = range(0, len(df.columns))

    return df


def plaquette_layout(backend, data_qubits, n_ancillas):
    # physical qubits for [data_0..data_3, ancilla_1..ancilla_n]: data qubits are fixed,
    # ancillas are the free qubits closest (summed distance) to the data qubits
    if backend is None or data_qubits is None:
        return None
    cm = backend.coupling_map
    free = [q for q in range(backend.num_qubits) if q not in data_qubits]
    free.sort(key=lambda q: (sum(cm.distance(q, d) for d in data_qubits), q))
    return list(data_qubits) + free[:n_ancillas]


def save_counts(path, counts, shots, backend, optimization_level, job_id, layout, initial_layout=None,
                seed_transpiler=None, compiled=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    record = {
        "backend": backend.name,
        "shots": shots,
        "optimization_level": optimization_level,
        "job_id": job_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "initial_layout": initial_layout,  # requested physical qubit for each virtual qubit (None = transpiler's choice)
        "layout": layout,  # physical qubit holding each virtual qubit at the end of the circuit
        "seed_transpiler": seed_transpiler,
        "compiled": compiled,  # gate counts / depth of the circuit that was actually executed
        "counts": counts,
    }
    with open(path, "w") as f:
        json.dump(record, f, indent=1)


def load_counts(path):
    # returns the normalized histogram {bitstring: probability}
    with open(path) as f:
        record = json.load(f)
    return {key: value/record["shots"] for key, value in record["counts"].items()}


def _execute(compiled_qc, shots, backend):
    if isinstance(backend, IBMBackend):
        sampler = Sampler(mode=backend)
        
        job = sampler.run([compiled_qc], shots=shots)
        result = job.result()[0]
        histogram = result.data.meas.get_counts()
    else: 
        # IBM fake backends and IQM backends (real or fake) support backend.run
        job = backend.run(compiled_qc, shots=shots)
        result = job.result()
        histogram = result.get_counts()    
    return job, histogram


def run_circuit(circuit:QuantumCircuit, shots, backend, optimization_level=0, save_path=None, initial_layout=None,
                retries=3, seed_transpiler=None):
    # reuse saved raw counts instead of re-running on hardware
    if save_path is not None and os.path.exists(save_path):
        print(f"loaded {save_path}")
        return load_counts(save_path)

    # fixed seed -> the same SWAP routing every time the circuit is compiled
    pm = generate_preset_pass_manager(optimization_level=optimization_level, backend=backend,
                                      initial_layout=initial_layout, seed_transpiler=seed_transpiler)
    compiled_qc = pm.run(circuit)
    print(backend.name)

    # a failed job (e.g. IQM "Internal server error") returns no counts: never save it, resubmit instead
    for attempt in range(1, retries + 1):
        job, histogram = _execute(compiled_qc, shots, backend)
        if isinstance(histogram, dict) and histogram:
            break
        print(f"job {job.job_id()} returned no counts (attempt {attempt}/{retries})")
    else:
        raise RuntimeError(f"no counts after {retries} attempts, nothing saved for {save_path}")

    if save_path is not None:
        layout = compiled_qc.layout.final_index_layout() if compiled_qc.layout else None
        compiled = {"ops": dict(compiled_qc.count_ops()), "depth": compiled_qc.depth(),
                    "num_2q_gates": compiled_qc.num_nonlocal_gates()}
        save_counts(save_path, histogram, shots, backend, optimization_level, str(job.job_id()), layout,
                    initial_layout, seed_transpiler, compiled)
    histogram = {key: value/shots for key, value in histogram.items()}
    return histogram
