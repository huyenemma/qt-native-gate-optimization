from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler


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
