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
# import torch
# from datetime import datetime



camera_id = 'cam3'
customer_id = '1005'  # Ganecos

# Path Define
basedir = os.path.abspath(os.path.dirname(__file__))
logs_folder = f'{basedir}/logs/'
device_video_path = f'{basedir}/{camera_id}_videos/'
device_video_json = f'{basedir}/{camera_id}_videos_json/un_uploaded_json/'
device_frames = f'{basedir}/{camera_id}_frames/'


# Defining logs
# logs_folder=f'{basedir}/logs/'
# logger.add(f"{logs_folder}{camera_id}_algo_object_detection.log", level="INFO", rotation="100 MB")


def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as Err:
        return False
    

def cal_area_of_rect(x1,y1,x2,y2):
    width = abs(x2-x1)
    height = abs(y2-y1)
    area =width * height
    print(f"Area : {area}")
    return area



def draw_boundary_box(video_id, video_path,video_date,video_time):
    """
    Draws bounding boxes on an image based on the results1.xyxy tensor from Ultralytics YOLOv8.

    Args:
        video_id : integer
        video_path : Video Location  
    """
    
    start_time = time.time()
    try:
        ################# Initialize the Video path ##################################
        cap = cv2.VideoCapture(video_path)
        Frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        Frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    

        object_Detection = {"object_data": []}

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps)

        
        if not cap.isOpened():
            exit()
            
        cfg = get_cfg()
        
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
        
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
        # cfg.MODEL.DEVICE = "cpu" 
        predictor = DefaultPredictor(cfg)
                
        
        frame_Number = 0

        while True:
            ret, frame = cap.read()
            frame_Number += 1
            

            if not ret:
                break
            
            if frame_Number % (int(frame_interval/2)) == 0 :
                # print(f"{frame_Number}")

                # Define the polygon vertices and this coordinates only apply on Cam3 
                vertices = np.array([[((169,154),(252,130), (292,152),(434,218),(431,366),(307,431),(286,358),(217,263),(199,188),(169,154))]], dtype=np.int32)


                # Create a mask with the polygon shape
                mask = np.zeros_like(frame)
                # cv2.imshow("frame",mask)
                cv2.fillPoly(mask, vertices, (255, 255, 255))

                # Extract the region of interest using the mask
                frame = cv2.bitwise_and(frame,mask)
                
                # if frame_Number ==12 :
                #     cv2.imwrite(f"/home/ubuntu/ganecos-backend1/new_version_1_1_1/cam3_detectron2_Model/cam3_frames/frame_12_{video_id}.jpg",frame)

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
                    if obj == 0 and float(confidence)>=0.60 :
                        pred_classes_names = metadata.thing_classes[obj]
                        Area = cal_area_of_rect(x1,y1,x2,y2)
                        create_json_data(object_Detection, frame_Number, x1,
                                    y1, x2, y2, confidence, pred_classes_names, video_id ,video_time,video_date,Area)
                        
                    else:
                        pass
                        
                    i+=1
                
                if frame_Number % frame_interval == 0:
                    video_time +=1
                        
    
        cap.release()
        ##########  Writing Json File ###########################
        json_file_path = f'{device_video_json}{camera_id}_{video_id}.json'
        create_json_file(json_file_path,object_Detection)


        ##########  Delete Video File ###########################
        # delete_file(video_path)
    except Exception as Err:
        print(f"Issue {Err}")
    finally:
        pass
        logger.info(f"Execution Time : {time.time() - start_time}")



def create_Video(out, frame):

  out.write(frame)

# Function for Creating Json

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

def create_json_data(object_Detection, frame_Number, x1, y1, x2, y2, confidence, Object, video_id,video_time,video_date,Area):
  
  dict = {
      "timeStamp": video_time,
      "dateStamp": video_date,
      "confidence": confidence,
      "object": Object,
      "co_ordinates": [x1, y1, x2, y2],
      "video_id": video_id,
      "frame_no": frame_Number,
      "Area" : Area

  }
  object_Detection["object_data"].append(dict)

 

# function for save frames


def save_frame(frame, frame_Number, video_id):

#   frame_folder_path=f'{device_frames}'
  frame_folder_path = f'{camera_id}_{video_id}'
  os.makedirs(os.path.join(device_frames, frame_folder_path), exist_ok=True)
  frame_path = f'{device_frames}{camera_id}_{video_id}/{camera_id}_{video_id}_{frame_Number}.jpg'
  cv2.imwrite(frame_path, frame)
  delete_file(frame_folder_path)



if __name__ =='__main__':
    try:

        if len(argv) <= 6 :
            video_id=int(argv[1])
            video_file_path=argv[2]
            video_date=int(argv[3])
            video_time=int(argv[4])
    
            draw_boundary_box(video_id,video_file_path,video_date,video_time)

    except IndexError:
        logger.warning('IndexError : Running in Wrong Way , No Argv Found')

    except ValueError:
        logger.warning("Issue In Video_id or Video_File_path")

    except Exception as E:
        logger.warning(f"Issue {E}")