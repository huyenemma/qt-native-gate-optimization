# Generate circuit type b 

- check `generate_circuit_b.py` for the json file creation: target qpu/simulator, noise model...
```commandline
./generate-circuit.sh $n
```
where n is the number of repetitions of plaquette 

# Submit and plot the result
- change appropriate `CIRCUIT_FILE`
```commandline
./run-and-plot.sh $KEY $n
```
where KEY is the API_KEY
