## Set up: 
- Give the right to run script: 
```chmod +x $bash_script_file_name```
- Export IONQ_API_KEY: 
```export KEY="copy_from_the_api"```
## How to run: 
- Submit the circuit:
```./submit-job.sh $KEY $name_of_json_file```
- Retrieve the result:
```./retrieve-job.sh $KEY $jod_id```
- Or retrieve and plot 2 histograms to compare from the results:
```./fetch-and-plot.sh $KEY $job_id_ideal_simulator $job_id_noisy_simulator```
## Change between ideal and noisy simulator: 
by setting the variable x in ` "noise": {"model":"$x"},` be `ideal` or `harmony`(or any name of ionq hardware)
