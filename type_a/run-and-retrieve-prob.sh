#!/bin/bash

KEY="$1"
FOLDER="$2"
NOISE="$3"
n=$4
SIMULATION_SCRIPT="./submit-job.sh"
RETRIEVE_SCRIPT="./retrieve-job.sh"

probabilities_of_0=()
job_ids=()

for ((i=1; i<=n; i++)); do
    CIRCUIT_FILE="${FOLDER}/${FOLDER}_${NOISE}_n${i}.json"

    # check if the circuit file exists
    if [ ! -f "$CIRCUIT_FILE" ]; then
        echo "$CIRCUIT_FILE does not exist, skipping..."
        continue
    fi

    echo "Submitting job with $CIRCUIT_FILE"
    submission_result=$($SIMULATION_SCRIPT $KEY $CIRCUIT_FILE)
    JOB_ID=$(echo $submission_result | jq -r '.id')
    job_ids+=($JOB_ID)

    sleep 20  # delay to wait for the job to be processed

    job_result=$($RETRIEVE_SCRIPT $KEY $JOB_ID)

    # Extract the probability of '0' from the histogram
    probability_of_0=$(echo $job_result | jq -r '.data.histogram["0"]')
    probabilities_of_0+=($probability_of_0)

    sleep 2  # Delay before the next iteration

done

# Convert the array of probabilities to a JSON array for Python processing
json_array=$(printf '%s\n' "${probabilities_of_0[@]}" | jq -R . | jq -s .)

echo "Probabilities of 0:"
for probability in "${probabilities_of_0[@]}"; do
    echo "$probability"
done

echo "All Job IDs:"
for job_id in "${job_ids[@]}"; do
    echo "$job_id"
done
