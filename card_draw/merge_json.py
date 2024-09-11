import json


def merge_json_files(file1, file2, output_file):
    # Load the contents of the first JSON file
    with open(file1, "r") as f1:
        data1 = json.load(f1)

    # Load the contents of the second JSON file
    with open(file2, "r") as f2:
        data2 = json.load(f2)

    # Merge the contents of the two JSON files by appending
    merged_data = {}
    for key in data1:
        if key in data2:
            if isinstance(data1[key], list) and isinstance(data2[key], list):
                merged_data[key] = data1[key] + data2[key]
            elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
                merged_data[key] = {
                    k: data1[key].get(k, []) + data2[key].get(k, [])
                    for k in set(data1[key]) | set(data2[key])
                }
            else:
                merged_data[key] = data2[key]
        else:
            merged_data[key] = data1[key]

    for key in data2:
        if key not in merged_data:
            merged_data[key] = data2[key]

    # Save the merged contents to the output JSON file
    with open(output_file, "w") as out_file:
        json.dump(merged_data, out_file, indent=4)


merge_json_files("cards.json", "new_cards.json", "cards.json")
