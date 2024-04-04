#!/bin/bash

# which circuit i wanna generate
version=$1
# Loop from 1 to 10
i=$2

echo "Generating circuit with n = $i"
python generate_circuit_${version}.py $i

echo "Finished generating circuits."
