import json
json_file_path = '/home/ubuntu/Try_code/Area_json/areas_of_rectangle.json'

with open(json_file_path,'r') as f:
    data =json.load(f)
    print(len(data["analysis_with_area"]))