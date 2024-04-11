import json
import os
import argparse


def add_sequence_4_cnot(control_qubit, qubits, circuit_data):

    circuit_data["body"]["circuit"].append(
        {"gate": "gpi2", "target": control_qubit, "phase": 0.25})

    for i in range(1, 5):
        target_qubit = qubits - 5 + i
        circuit_data["body"]["circuit"].append(
            {"gate": "ms", "targets": [control_qubit, target_qubit], "phases": [0, 0]})
        circuit_data["body"]["circuit"].append({"gate": "gpi2", "target": control_qubit, "phase": 0.5})
        circuit_data["body"]["circuit"].append({"gate": "gpi2", "target": target_qubit, "phase": 0.5})

    circuit_data["body"]["circuit"].append(
        {"gate": "gpi2", "target": control_qubit, "phase": -0.25})


def generate_circuit(name, n, target, noise):
    qubits = 5

    circuit_data = {
        "lang": "json",
        "shots": 1000,
        "target": target,
        "noise": {"model": noise},
        "name": "b2_" + noise + "_" + name,
        "body": {
            "gateset": "native",
            "qubits": qubits,
            "circuit": []
        }
    }

    for i in range(1, n+1):
        add_sequence_4_cnot(0, qubits, circuit_data)

    output_dir = "b2"
    os.makedirs(output_dir, exist_ok=True)

    # Save to file
    file_name = f"{output_dir}/{output_dir}_{noise}_{name}.json"
    with open(file_name, 'w') as json_file:
        json.dump(circuit_data, json_file, indent=4)

    print(f"JSON file '{file_name}' generated successfully.")


def main():
    parser = argparse.ArgumentParser(description='Generate a quantum circuit JSON file.')
    parser.add_argument('n', type=int, help='Number of repetitions for the circuit.')
    args = parser.parse_args()

    # Generate circuit with n from command-line argument
    for i in range(1, args.n + 1):
        generate_circuit(f"n{i}", i, "simulator", "harmony")


if __name__ == "__main__":
    main()

