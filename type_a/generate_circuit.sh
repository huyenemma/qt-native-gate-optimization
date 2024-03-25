#!/bin/bash

# Loop from 1 to 10
i=$1
echo "Generating circuit with n = $i"
python generate_circuit_v2.py $i

echo "Finished generating circuits."
