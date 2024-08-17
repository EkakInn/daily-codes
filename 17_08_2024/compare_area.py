import json 
from loguru import logger #Logger Modules Import

def detectron_data():
    list_of_detectron_data =[]
    with open('//home/ubuntu/Try_code/camera_ip_101/json/detectron_cam_ip_101_with_area.json','r') as file :
        detectron_data = json.load(file)
        length_detectron_data = len(detectron_data['object_data'])

    for i in range(length_detectron_data-1) :
        timestamp =detectron_data['object_data'][i]['timeStamp']
        datestamp = detectron_data['object_data'][i]['dateStamp']
        confidence = detectron_data['object_data'][i]['confidence']
        object = detectron_data['object_data'][i]['object']
        co_ordinates = detectron_data['object_data'][i]['co_ordinates']
        video_id = detectron_data['object_data'][i]['video_id']
        frame = detectron_data['object_data'][i]['frame_no']
        area = detectron_data['object_data'][i]['Area']
        


        list_of_detectron_data.append([timestamp,datestamp,confidence,object,co_ordinates,video_id,frame,area])
    
    return list_of_detectron_data
    


def yolov5_data():
    list_of_yolov5_data =[]
    with open('/home/ubuntu/Try_code/camera_ip_101/json/yolov5_cam_ip_101_object.json','r') as file :
        yolov5_data = json.load(file)
        length_yolov5_data = len(yolov5_data['object_data'])

    for i in range(length_yolov5_data-1) :
        timestamp =yolov5_data['object_data'][i]['timeStamp']
        datestamp = yolov5_data['object_data'][i]['dateStamp']
        confidence = yolov5_data['object_data'][i]['confidence']
        object = yolov5_data['object_data'][i]['object']
        co_ordinates = yolov5_data['object_data'][i]['co_ordinates']
        video_id = yolov5_data['object_data'][i]['video_id']
        frame = yolov5_data['object_data'][i]['frame_no']
        area = yolov5_data['object_data'][i]['Area']
        list_of_yolov5_data.append([timestamp,datestamp,confidence,object,co_ordinates,video_id,frame,area])
    
    return list_of_yolov5_data
    

def cal_percentage_difference(detectron_area,yolov5_area):  
    difference = max(detectron_area,yolov5_area) - min(detectron_area,yolov5_area)
    Average = (detectron_area + yolov5_area)/2
    ratio = difference/Average
    percentage_difference = round(ratio * 100)

    return percentage_difference


def create_json_file(json_file_path,json_data):
    status=False
    try:
        with open(json_file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        status=True
    except Exception as Err:
        status=False
    finally:
        return status
    

def create_json_data(object_Detection, frame_Number, coordinates, confidence, Object,area, video_id,video_time,video_date):
  
  dict = {
      "timeStamp": video_time,
      "dateStamp": video_date,
      "confidence": confidence,
      "object": Object,
      "co_ordinates": coordinates,
      "video_id": video_id,
      "frame_no": frame_Number,
      "Area" : area

  }
  object_Detection["object_data"].append(dict)



def cal_percentage_difference_coordinates(detectron_coordinates,yolov5_coordinates):

    difference = max(detectron_coordinates[0],yolov5_coordinates[0]) - min(detectron_coordinates[0],yolov5_coordinates[0])
    Average = (detectron_coordinates[0] + yolov5_coordinates[0])/2
    ratio = difference/Average
    percentage_difference = round(ratio * 100)

    return percentage_difference

    

# with open('/home/ubuntu/Try_code/camera_ip_101/json/detectron_cam_ip_101_with_area.json','r') as file_1 :
#     yolov5_data = json.load(file_1)
    
list_detectron = detectron_data()
list_yolov5 = yolov5_data()
# print(len(list_yolov5))
# print(list_detectron)


object_Detection = {"object_data": []}
j =0
try:
    for i in range(0,len(list_detectron)):

        detectron_frame = list_detectron[i][6]
        detectron_area = list_detectron[i][7]
        detectron_coordinates = list_detectron[i][4]
        detectron_timeStamp = list_detectron[i][0]
        detectron_DateStamp = list_detectron[i][1]
        detectron_confidence = list_detectron[i][2]
        detectron_object = list_detectron[i][3]
        detectron_video_id = list_detectron[i][5]

        for j in range(len(list_yolov5)):
            yolov5_frame = list_yolov5[j][6]
            yolov5_area = list_yolov5[j][7]
            yolov5_coordinates = list_yolov5[j][4]
            # print(j)
        # print(f"detectron_frame{detectron_frame},yolov5_frame{yolov5_frame}")
            if detectron_frame == yolov5_frame:
                area_percentage = cal_percentage_difference(detectron_area,yolov5_area)
                coordinates_percentage = cal_percentage_difference_coordinates(detectron_coordinates,yolov5_coordinates)
                # j+=1

                # print(coordinates_percentage)
                if area_percentage < 20 and coordinates_percentage < 20 :
                    # print(percentage)
                    create_json_data(object_Detection,detectron_frame,detectron_coordinates,detectron_confidence,detectron_object,detectron_area,detectron_video_id,detectron_timeStamp,detectron_DateStamp)
                
            
except Exception as Err:
        logger.exception(f'Issue in Compare Json {Err}')

json_file_path ='/home/ubuntu/Try_code/camera_ip_101/json/compare_area_2.json'

create_json_file(json_file_path,object_Detection)