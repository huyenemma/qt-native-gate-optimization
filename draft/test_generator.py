import json

def compare_json_files(file1, file2):
    with open(file1, 'r') as f:
        data1 = json.load(f)

    with open(file2, 'r') as f:
        data2 = json.load(f)

    return data1 == data2


file1 = 'v2_generated_2.json'
file2 = 'v2_manual_2.json'
if compare_json_files(file1, file2):
    print("The JSON files are the same")
else:
    print("The JSON files are different")
