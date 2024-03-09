import json

def compare_json_files(file1, file2):
    with open(file1, 'r') as f:
        data1 = json.load(f)

    with open(file2, 'r') as f:
        data2 = json.load(f)

    return data1 == data2


file1 = 'test2.json'
file2 = 'test2_generated.json'
if compare_json_files(file1, file2):
    print("The JSON files are the same")
else:
    print("The JSON files are different")
