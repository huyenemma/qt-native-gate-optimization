
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime import SamplerV2 as Sampler
import fresh as fresh
import recycle as recycle


def run_circuit(n, shots, backend, type, optimization_level=0):
    if type == "fresh":
        qc = fresh.generate_circuit(n)
    elif type == "recycle":
        qc = recycle.generate_circuit(n)
    
    pm = generate_preset_pass_manager(optimization_level=optimization_level, backend=backend)
    compiled_qc = pm.run(qc)
    
    sampler = Sampler(mode=backend)
    
    job = sampler.run([compiled_qc], shots=shots)
    result = job.result()[0]
    histogram = result.data.meas.get_counts()
    #print(histogram)
    #histogram = result.get_counts(qc)
    histogram = {key: value/shots for key, value in histogram.items()}
    return histogram
