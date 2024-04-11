#!/bin/bash

# which circuit i wanna generate
version=$1
# Loop from 1 to 10
i=$2
target=$3
noise=$4

echo "Generating circuit with n = $i"
python generate_circuit_${version}.py $i $target $noise

echo "Finished generating circuits."
