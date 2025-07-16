# Optimizing plaquette circuit at native gate on IonQ API
This repo is part of Bachelor's thesis writing at Aalto University 

Executing circuits with different number of plaquette circuit repetitions in 2 approach: 
- Type A: use fresh new ancilla qubit for repetitions 
- Type B: use the same ancilla qubit for repetitions

All the source code for generate 3 stage of optimization of these 2 types are in each folder `./type_a` and `./type_b`

## Change directory to type_a or type_b 
## Command to generate circuits
```commandline
./generate-circuit.sh $which_type $number_of_repetition $target $noise_model
```
- which_type: the type of circuit you want t generate. 
Can be `a1, a2, a3` in type_a folder, or `b1, b2, b3` in type_b folder
- number_of_repetition:  n
- target: `simulator` / `qpu.aria1`
- noise_model: `harmony`, `aria1`, `qpu-aria1`, `qpu-harmony` 

## Run and get the prob of ancilla qubit = 1: 

```commandline
./run-and-retrieve-prob.sh $KEY $which_type $noise_model $number_of_repetition
```
where $KEY is the API_KEY from IONQ 

## Know the job_id, get probability result: 
- copy all job_ids into `job_ids.txt`, leave a blank line as the last line of the file 
```commandline
./get_ancilla_meas_a.sh $KEY 
``` 

