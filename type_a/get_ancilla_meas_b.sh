#!/bin/bash

KEY="$1"
JOB_IDS_FILE="job_ids.txt"  # The file containing the list of job IDs

# Check if the job IDs file exists
if [ ! -f "$JOB_IDS_FILE" ]; then
    echo "Job IDs file does not exist: $JOB_IDS_FILE"
    exit 1
fi

n=0
probs=()
# Iterate over each job ID in the file and collect histograms
while IFS= read -r JOB_ID; do
    # Ensure the JOB_ID is not empty
    if [ -z "$JOB_ID" ]; then
        continue
    fi

    ((n++))

    job_result=$(./retrieve-job.sh $KEY $JOB_ID)
    if [ $? -ne 0 ]; then
        echo "Failed to retrieve job $JOB_ID"
        continue
    fi

    # Extract the histogram as a JSON string
    histogram=$(echo $job_result | jq -r '.data.histogram | @json')
    if [ "$histogram" == "null" ]; then
        echo "Histogram not found for job $JOB_ID"
        continue
    fi

    name=$(echo $job_result | jq -r '.data.name | @json')
    #echo "Histogram for job $JOB_ID: $histogram"


    # Pass the histogram to the Python script for calculation
    prob_ancillas=$(echo $histogram | python3 ancilla_meas.py --n "$n" --name "$name")
    #echo "Probabilities for job $JOB_ID: $prob_ancillas"
    probs+=("$prob_ancillas")

done < "$JOB_IDS_FILE"

for prob_array in "${probs[@]}"; do
    echo "$prob_array"
done