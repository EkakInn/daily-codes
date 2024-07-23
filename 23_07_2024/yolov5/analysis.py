from ultralytics import YOLO
import cv2

model = torch.hub.load('ultralytics/yolov5',
                               'yolov5s', pretrained=True)

image_path = '/home/ubuntu/Try_code/cam3_frames/frame_5025.jpg'

image = cv2.imread(image_path)

results2 = model(image)

print(results2)
xyxy = results2.xyxy[0].gpu().numpy()


for box in xyxy:
    
    # Extract coordinates (assuming normalized format)
    x1, y1, x2, y2 = int(box[0]), int(
        box[1]), int(box[2]), int(box[3])
    print(x1,x2)
    cv2.rectangle(image, (x1, y1), (x2, y2),
                    (0, 0, 255), 2)  # Red for boxes
    # Object = results2.crop()[0]["label"][:-5]
    # confidence = results2.crop()[0]["label"][-4:]
