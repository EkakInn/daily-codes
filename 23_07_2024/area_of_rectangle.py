import json
import os

# define function for calculate area of reactangle 
def cal_area_of_rect(coordinates):
    x1 ,y1,x2,y2=coordinates
    width = abs(x2-x1)
    height = abs(y2-y1)
    area =width * height
    print(f"Area : {area}")
    return area

Area = {"analysis_with_area":[]}

# Specify the directory you want to scan
directory_path = '/home/ubuntu/Try_code/json'

# Get a list of all files and directories in the specified path
all_files = os.listdir(directory_path)

# Filter out only files (excluding directories)
file_names = [f for f in all_files if os.path.isfile(os.path.join(directory_path, f))]

# Print the list of file names
print(file_names)

for file_name in file_names: 

    all_area=[]
    with open(f'/home/ubuntu/Try_code/json/{file_name}','r') as file :
        data = json.load(file)
        # print(len(data["object_data"]))
        n=len(data["object_data"])
        for i in range(n):
            coordinates=data["object_data"][i]['co_ordinates']
            # print(coordinates,end=' ')
            # Area=data["object_data"][i]['Area']
            all_area.append(cal_area_of_rect(coordinates))
        video_id = data["object_data"][0]['video_id']

    maximum_area = max(all_area)
    minimum_area = min(all_area)
    average_area = sum(all_area)//len(all_area)

    # print(F'Maximum Area {maximum_area}')
    # print(F'Minimum Area {minimum_area}')
    # print(F'Average Area {average_area}')

    dict = {
        "video_id": video_id,
        "Maximum_Area": maximum_area,
        "Minimum_Area":minimum_area,
        "Average_Area":average_area

    }

    Area["analysis_with_area"].append(dict)

with open(f'/home/ubuntu/Try_code/Area_json/areas_of_rectangle.json', "w") as json_file:
        json.dump(Area, json_file, indent=4)
    

