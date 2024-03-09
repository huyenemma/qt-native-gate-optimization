#!/bin/bash

# Loop from 1 to 10
for i in {1..10}
do
  echo "Generating circuit with n = $i"
  python generate_circuit.py $i
done

echo "Finished generating circuits."
