#!/bin/bash

# Loop from 1 to 10
i=10
echo "Generating circuit with n = $i"
python generate_circuit.py $i

echo "Finished generating circuits."
