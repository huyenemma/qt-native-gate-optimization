#!/bin/bash

KEY="$1"
JOB_ID_NO_NOISE="$2"
JOB_ID_NOISY="$3"

no_noise_result=$(./retrieve-job.sh $KEY $JOB_ID_NO_NOISE)
noisy_result=$(./retrieve-job.sh $KEY $JOB_ID_NOISY)

# -r flag for raw output
no_noise_histogram=$(echo $no_noise_result | jq -r '.data.histogram')
noisy_histogram=$(echo $noisy_result | jq -r '.data.histogram')

python3 plot_histogram.py "$no_noise_histogram" "$noisy_histogram"