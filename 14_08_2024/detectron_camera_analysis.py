import os
import cv2
import numpy as np
# from ultralytics import YOLO  # pip install ultralytics==8.0.232
import torch  # pip install torch == 2.2.2
import json
from datetime import datetime
from sys import argv  # argument Variable take input from when file running
from  loguru import logger
import random

# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
# setup_logger()

# import some common libraries
# import numpy as np
# import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
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
    
    if frame_Number % (int(frame_interval/2))==0:
    
        cfg = get_cfg()
        
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
        
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
        # cfg.MODEL.DEVICE = "cpu" 
        predictor = DefaultPredictor(cfg)
                
        # vertices = np.array([[((338,231),(618,399), (998,383),(1015,263),(1193,237),(1276,234),(1300,352),(1622,338),(1548,252),(1714,184),(2551,642),(2545,1428),(25,1428),(4,376),(339,231),(605,220),(338,231))]], dtype=np.int32)


        # # Create a mask with the polygon shape
        # mask = np.zeros_like(frame)
        # # cv2.imshow("frame",mask)
        # cv2.fillPoly(mask, vertices, (255, 255, 255))

        # # Extract the region of interest using the mask
        # image = cv2.bitwise_and(frame,mask)
        outputs = predictor(frame)

        
        label = outputs["instances"].pred_classes
        Boxes = outputs["instances"].pred_boxes
        scores = outputs["instances"].scores
        
        i = 0
        for box in Boxes:
            
            x1 = int(box[0].item())
            y1 = int(box[1].item())
            x2 = int(box[2].item())
            y2 = int(box[3].item())
            
            conf = scores[i].item()
            confidence = f'{conf :.2f}'
            obj = label[i].item()
            print(obj)
            if  obj ==0 and float(confidence)>=0.60:
                pred_classes_names = metadata.thing_classes[obj]
                # cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
                # cv2.putText(image, pred_classes_names, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                create_json_data(object_Detection, frame_Number, x1,
                                            y1, x2, y2, confidence, pred_classes_names, video_id=101 ,video_time =183500,video_date=20220819)
                print("json added")


cap.release()

json_file_path='/home/ubuntu/Try_code/camera_ip_101/json/detectron_cam_ip_101_2.json'  
create_json_file(json_file_path,object_Detection)

logger.info(f"Execution Time : {time.time() - start_time}")