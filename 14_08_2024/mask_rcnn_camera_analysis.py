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
import time 



start_time = time.time()



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

def create_json_data(object_Detection, frame_Number, x1, y1, x2, y2, confidence, Object, video_id,video_time,video_date):
  
  dict = {
      "timeStamp": video_time,
      "dateStamp": video_date,
      "confidence": confidence,
      "object": Object,
      "co_ordinates": [x1, y1, x2, y2],
      "video_id": video_id,
      "frame_no": frame_Number

  }
  object_Detection["object_data"].append(dict)



video_path = '/home/ubuntu/Try_code/camera_ip_101/videos/camera_ip_101_2 - Made with Clipchamp.mp4'

cap = cv2.VideoCapture(video_path)

Frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
Frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))



object_Detection = {"object_data": []}

fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps)

frame_Number =0
while True :
    ret , frame = cap.read()
    frame_Number+=1

    if not ret :
         break
    
    try :        
            
            if frame_Number % (int(frame_interval/2)) == 0:
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

                # # vertices = np.array([[((612,408),(979,414), (820,1385),(29,1385),(344,773),(612,408))]], dtype=np.int32)
                # vertices = np.array([[((338,231),(618,399), (998,383),(1015,263),(1193,237),(1276,234),(1300,352),(1622,338),(1548,252),(1714,184),(2551,642),(2545,1428),(25,1428),(4,376),(339,231),(605,220),(338,231))]], dtype=np.int32)
                # # Create a mask with the polygon shape
                # mask = np.zeros_like(frame)
                # # cv2.imshow("frame",mask)
                # cv2.fillPoly(mask, vertices, (255, 255, 255))

                # # Extract the region of interest using the mask
                # image = cv2.bitwise_and(frame,mask)

                transform = T.Compose([T.ToTensor()])
                image_tensor = transform(frame)

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
                        x1  = int(box[2].item())
                        y2= int(box[0].item())
                        y1 = int(box[1].item())
                        x2 = int(box[3].item())
                        co_ordinates= [x1,y1,x2,y2]
                        object  = COCO_INSTANCE_CATEGORY_NAMES[filtered_labels[i]]
                        confidence = filtered_scores[i].item()
                        create_json_data(object_Detection, frame_Number, x1,
                                            y1, x2, y2, confidence, object, video_id=101 ,video_time =183500,video_date=20220819)
                        print("json added")
                        # cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
                        # cv2.putText(image, object, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # cv2.imwrite('/home/ubuntu/Try_code/camera_ip_101/predict_frames/camera_ip_101_4.jpg',image)

                   
    except Exception as Err:
        logger.exception(f'Issue in analysis_by_Mask_R_CNN {Err}')

cap.release()

json_file_path='/home/ubuntu/Try_code/camera_ip_101/json/cam_ip_101.json'  
create_json_file(json_file_path,object_Detection)

logger.info(f"Execution Time : {time.time() - start_time}")



