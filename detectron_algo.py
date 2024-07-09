import cv2
# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
# setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random
# from google.colab.patches import cv2_imshow

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import time
import torch
from datetime import datetime

object_detection ={"Object" : []}
start_time = time.time()
video_path = 'scenario3_1 (online-video-cutter.3qPV3BXW.com).mp4.part'
cap = cv2.VideoCapture(video_path)

Frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
Frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval=int(fps)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (Frame_width,Frame_height))


cfg = get_cfg()
# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
predictor = DefaultPredictor(cfg)

frame_number = 0
while True:
    ret, frame = cap.read()
    frame_number+=1
    if not ret:
        break


    # Define the polygon vertices
    vertices = np.array([[((367,272),(526,224), (898,366),(918,579),(620,675),(620,594),(429,399),(404,305),(367,272))]], dtype=np.int32)

    # Create a mask with the polygon shape
    mask = np.zeros_like(frame)
    # cv2.imshow("frame",mask)
    cv2.fillPoly(mask, vertices, (255, 255, 255))

    # Extract the region of interest using the mask
    resized_frame = cv2.bitwise_and(frame,mask)
    # cv2.imwrite('frame.jpg',resized_frame)
    # break
    outputs = predictor(resized_frame)
    # v = Visualizer(frame[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    # out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    # result = out.get_image()[:, :, ::-1]
    # print(result)
    print(outputs)
    label = outputs["instances"].pred_classes
    Boxes = outputs["instances"].pred_boxes
    scores = outputs["instances"].scores
    # print(label)
    # print(Boxes)
    # print(scores)
    i = 0
    for box in Boxes:
        # x1, y1, x2, y2 = box.item()
        x1 = int(box[0].item())
        y1 = int(box[1].item())
        x2 = int(box[2].item())
        y2 = int(box[3].item())
        # print(x1,y1,x2,y2)
        # print(box)
        conf = scores[i].item()
        confidence = f'{conf :.2f}'
        obj = label[i].item()
        if obj == 0 and float(confidence)>=0.60:
          pred_classes_names = metadata.thing_classes[obj]
          print(pred_classes_names)

          # print(conf)
        # print(a:.2f)
          # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
          # cv2.putText(frame, confidence , (int(x1), int(y1)- 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

          timestamp = datetime.now().strftime('%d/%m/%Y_%')
          timestamp = datetime.now().strftime('%d/%m/%Y_%H:%M:%S')
          dict = {
          "Frame_Number" : frame_number,
          "TimeStamp" : timestamp,
          "Object" : pred_classes_names,
          "Coordinates" : [x1,y1,x2,y2],
          "Confidence" : float(confidence)
          }
          object_detection["Object"].append(dict)
          print(type(confidence))
        i+=1
    # cv2_imshow(frame)

    # out.write(frame)




out.release()
cap.release()
print("--- %s seconds ---" % (time.time() - start_time))

with open("object.json", "w") as json_file:
    json.dump(object_detection, json_file, indent=3)
