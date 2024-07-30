# Import the modules 
import os 
import json
import torch
import torchvision
from PIL import Image
import torchvision.transforms as T
from torchvision.models.detection import maskrcnn_resnet50_fpn
import cv2
import numpy as np
from loguru import logger #Logger Modules Import


camera_id='cam3'
customer_id='1005' #Ganecos

# Path Define
basedir=os.path.abspath(os.path.dirname(__file__))
device_videos_jsons = f'{basedir}/{camera_id}_videos_json/un_uploaded_json'
device_video_frames = f'{basedir}/{camera_id}_frames/'




# define function to create folder
def folder_creation(folder_name):
    try:
        logger.info('_Folder Creation Started')
        os.makedirs(folder_name,exist_ok=True)
        logger.info(f"_Folder Created {folder_name}")
    except Exception as Err:
        logger.warning(f'Issue in Folder Creation {Err}')


# define function to generate the file names in list
def List_of_json_files_names(device_videos_jsons):

    try:

        # Get a list of all files and directories in the specified path
        all_files = os.listdir(device_videos_jsons)

        # Filter out only files (excluding directories)
        file_names = [f for f in all_files if os.path.isfile(os.path.join(device_videos_jsons, f))]

    except Exception as Err:
        logger.warning(f'Issue in List_of_json_files_names {Err}')

    return file_names



# define function for calculate area of reactangle 
def calculate_area_of_rectangle(coordinates):

    try :
        x1 ,y1,x2,y2 = coordinates
        width = abs(x2-x1)
        height = abs(y2-y1)
        area =width * height
        print(f"Area : {area}")
    
    except Exception as Err:
        logger.warning(f'Issue in calculate_area_of_rectangle {Err}')

    return area

# define function for calculate average
def calculate_average_area_of_rectangle(video_id):

    try:
        video_json_file_path =f'{basedir}/{camera_id}_videos_json/un_uploaded_json/{camera_id}_{video_id}.json'
        with open(video_json_file_path,'r') as f:
            data = json.load(f)
        length_of_data = len(data["object_data"])
        List_of_area = []
        for i in range(length_of_data):
            Area=data["object_data"][i]['Area']
            frame_number=data["object_data"][i]['frame_no']
            List_of_area.append(Area)
        average_area_of_rectangle = sum(List_of_area)//length_of_data

    except Exception as Err:
        logger.warning(f'Issue in calculate_average_area_of_rectangle {Err}')

    return average_area_of_rectangle


# define function for generate the List of error frames
def List_of_error_frames(average_area_of_rectangle,video_id):


    try: 
        video_json_file_path =f'{basedir}/{camera_id}_videos_json/un_uploaded_json/{camera_id}_{video_id}.json'
        with open(video_json_file_path,'r') as f:
            data = json.load(f)
        length_of_data = len(data["object_data"])
        List_of_error_frame_Number = []
        for i in range(length_of_data):
            Area_of_rectangle=data["object_data"][i]['Area']
            frame_number=data["object_data"][i]['frame_no']
            if (2 * average_area_of_rectangle) < Area_of_rectangle: 
                List_of_error_frame_Number.append(frame_number)

    except Exception as Err:
        logger.warning(f'Issue in List_of_error_frames {Err}')
    

    return List_of_error_frame_Number

# define function for save error frames in a folder
def Save_frame(list_of_error_frames,video_path,image_folder_path):
    try:
        cap = cv2.VideoCapture(video_path)
        i=0 
        frame_count=0
        while True:
            ret ,frame = cap.read()
            frame_count+=1

            if not ret :
                break

            if list_of_error_frames[i] == frame_count :
                cv2.imwrite(f'{image_folder_path}{frame_count}.jpg',frame)
                print(f"save_frame : {list_of_error_frames[i]}")
                # print(f"Video_frame : {frame_count}")
                i+=1
            
            # print(frame_count)
        cap.release()

    except Exception as Err:
        logger.warning(f'Issue in List_of_error_frames {Err}')

# define function for analysis using Mask R-CNN Model
def analysis_by_Mask_R_CNN(video_path,video_id,List_of_error_frames,error_frame_json,video_timestamp,video_datestamp,error_frames_json_folder_path):
    
    try :
        image_folder_path = f'{basedir}/{camera_id}_frames/{video_id}/'
        folder_creation(image_folder_path)
        folder_creation(error_frames_json_folder_path)
        Save_frame(List_of_error_frames,video_path,image_folder_path)

        # Load the COCO class names
        COCO_INSTANCE_CATEGORY_NAMES = [
            '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter',
            'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
            'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
            'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
            'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
            'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
            'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
            'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
            'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
            'teddy bear', 'hair drier', 'toothbrush'
        ]

        # Load the pre-trained Mask R-CNN model
        model = maskrcnn_resnet50_fpn(pretrained=True)
        model.eval()
        
        for Error_frames in List_of_error_frames:
        # Load the image
            image_path = f'{basedir}/{camera_id}_frames/{video_id}/{Error_frames}.jpg'

        

            image = cv2.imread(image_path)

            vertices = np.array([[((169,154),(252,130), (292,152),(434,218),(431,366),(307,431),(286,358),(217,263),(199,188),(169,154))]], dtype=np.int32)
            # Create a mask with the polygon shape
            mask = np.zeros_like(image)
            # cv2.imshow("frame",mask)
            cv2.fillPoly(mask, vertices, (255, 255, 255))

            # Extract the region of interest using the mask
            image = cv2.bitwise_and(image,mask)

            transform = T.Compose([T.ToTensor()])
            image_tensor = transform(image)

        # Perform detection
            with torch.no_grad():
                prediction = model([image_tensor])

            # Extract bounding boxes, labels, and scores
            boxes = prediction[0]['boxes']
            labels = prediction[0]['labels']
            scores = prediction[0]['scores']

            # Set a threshold for detection
            threshold = 0.6
            filtered_indices = [i for i, score in enumerate(scores) if score > threshold]
            filtered_boxes = boxes[filtered_indices]
            filtered_labels = labels[filtered_indices]
            filtered_scores = scores[filtered_indices]

            for i in range(len(filtered_boxes)):
                if filtered_labels[i] == 1:
                    box = filtered_boxes[i]
                    x1 = int(box[0].item())
                    y1 = int(box[1].item())
                    x2 = int(box[2].item())
                    y2 = int(box[3].item())
                    object  = COCO_INSTANCE_CATEGORY_NAMES[filtered_labels[i]]
                    confidence = filtered_scores[i].item()
                    dict ={
                        "timeStamp": video_timestamp,
                        "dateStamp": video_datestamp,
                        "confidence": round(confidence,2) ,
                        "object": object,
                        "co_ordinates": [x1,y1,x2,y2],
                        "video_id": video_id,
                        "frame_no": Error_frames,
                    }
                    error_frame_json["object_detection"].append(dict)
           
            

            with open(f'{error_frames_json_folder_path}Mask_R_CNN_{video_id}.json','w') as json_file:
                json.dump(error_frame_json,json_file,indent=4)

    except Exception as Err:
        logger.warning(f'Issue in analysis_by_Mask_R_CNN {Err}')








