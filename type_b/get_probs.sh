#!/bin/bash

KEY="$1"
JOB_IDS_FILE="job_ids.txt"  # The file containing the list of job IDs

probabilities_of_0=()
# Check if the job IDs file exists
if [ ! -f "$JOB_IDS_FILE" ]; then
    echo "Job IDs file does not exist: $JOB_IDS_FILE"
    exit 1
fi

# Iterate over each job ID in the file
while IFS= read -r JOB_ID; do
    # Ensure the JOB_ID is not empty
    if [ -z "$JOB_ID" ]; then
        continue
    fi

    job_result=$(./retrieve-job.sh $KEY $JOB_ID)
    if [ $? -ne 0 ]; then
        echo "Failed to retrieve job $JOB_ID"
        continue
    fi

    probability_of_0=$(echo $job_result | jq -r '.data.histogram["0"]')
    if [[ $probability_of_0 == "null" || -z $probability_of_0 ]]; then
        echo "Probability of '0' not found for job $JOB_ID"
        continue
    fi
    probabilities_of_0+=($probability_of_0)

done < "$JOB_IDS_FILE"

echo "Probabilities of 0:"
for probability in "${probabilities_of_0[@]}"; do
    echo "$probability"
done
