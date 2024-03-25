import cirq
import cirq_ionq as ionq
from cirq_ionq.ionq_native_gates import GPIGate, GPI2Gate, MSGate

q0, q1, q2, q3, q4 = cirq.LineQubit.range(5)


circuit = cirq.Circuit([
    GPI2Gate(phi=0.25).on(q0),
    MSGate(phi0=0, phi1=0).on(q0, q1),
    GPI2Gate(phi=0.5).on(q1),
    MSGate(phi0=0, phi1=0).on(q0, q2),
    GPI2Gate(phi=0.5).on(q2),
    MSGate(phi0=0, phi1=0).on(q0, q3),
    GPI2Gate(phi=0.5).on(q3),
    MSGate(phi0=0, phi1=0).on(q0, q4),
    GPI2Gate(phi=0.5).on(q4),
    GPI2Gate(phi=-0.25).on(q0),
    cirq.measure(q0, key='x')
])
print(circuit)

service = ionq.Service(api_key="FODJkqf8GZf5jCNTpzMviWE03QqEH7yN")
result = service.run(circuit=circuit, repetitions=1024, target="simulator")
histogram = result.histogram(key='x')
print(histogram)




