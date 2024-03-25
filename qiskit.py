from qiskit import QuantumCircuit
import qiskit_ionq

from qiskit_ionq import GPIGate, GPI2Gate, MSGate

provider = qiskit_ionq.IonQProvider()
backend = provider.get_backend("ionq_simulator")
backend.set_options(noise_model="harmony")

circuit = QuantumCircuit(5, 1)

circuit.append(GPI2Gate(0.25), [0])
circuit.append(MSGate(0, 0), [0, 1])
circuit.append(GPI2Gate(0.5), [1])
circuit.append(MSGate(0, 0), [0, 2])
circuit.append(GPI2Gate(0.5), [2])
circuit.append(MSGate(0, 0), [0, 3])
circuit.append(GPI2Gate(0.5), [3])
circuit.append(MSGate(0, 0), [0, 4])
circuit.append(GPI2Gate(0.5), [4])
circuit.append(GPI2Gate(-0.25), [0])
circuit.draw()

job = backend.run(circuit)
print(job.result().get_counts())
