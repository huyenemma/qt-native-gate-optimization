#!/bin/bash

KEY="$1"
CIRCUIT_FILE="$2"
SIMULATION_SCRIPT="./submit-job.sh"
RETRIEVE_SCRIPT="./retrieve-job.sh"

probabilities_of_0=()
n=10
# run the simulation n times
for ((i=1; i<=n; i++)); do
    # submit the simulation job and retrieve the job ID from the JSON output
    submission_result=$($SIMULATION_SCRIPT $KEY $CIRCUIT_FILE)
    JOB_ID=$(echo $submission_result | jq -r '.id')

    sleep 5

    job_result=$($RETRIEVE_SCRIPT $KEY $JOB_ID)

    # extract the probability of '0' from the histogram
    probability_of_0=$(echo $job_result | jq -r '.data.histogram["0"]')

    probabilities_of_0+=($probability_of_0)

    sleep 5

done

# convert the array of probabilities to a JSON array for Python processing
json_array=$(printf '%s\n' "${probabilities_of_0[@]}" | jq -R . | jq -s .)

python3 plot_histogram.py "$json_array"
