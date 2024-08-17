import cv2
import json
import time 
from loguru import logger #Logger Modules Import

def draw_video_coordinates(video_path,uploaded_video_path,meta_data,file_name):
   
    start_time = time.time()
    logger.info("_Draw Co-ordinates on Video Code Started")
    
    try:
        frame_count = 0 # Frame_Number Varaible is used for Checking Frame Number
        cap = cv2.VideoCapture(video_path) # get the video 

        Frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # get the frame width 
        Frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # get the frame height 
        
        
        fps = cap.get(cv2.CAP_PROP_FPS) # get the frame per second 
        frame_interval=int(fps) # convert fps into integer
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Initalize which format while upload the video in dbx
        out = cv2.VideoWriter(f'{uploaded_video_path}', fourcc, fps, (Frame_width,Frame_height)) 
               
            
        value = 0 
        
         #  vertices = np.array([[((367,272),(526,224), (898,366),(918,579),(620,675),(620,594),(429,399),(404,305),(367,272))]], dtype=np.int32)

        while True :
            ret , frame = cap.read() # read video frames 
            frame_count +=1 # point to video frames
            
            # draw box on Area of Interest 
            # cv2.line(frame,(169,154),(252,130),(0,0,255),2)
            # cv2.line(frame,(252,130),(292,152),(0,0,255),2)
            # cv2.line(frame,(292,152),(434,218),(0,0,255),2)
            # cv2.line(frame,(434,218),(431,366),(0,0,255),2)
            # cv2.line(frame,(431,366),(307,431),(0,0,255),2)
            # cv2.line(frame,(307,431),(286,358),(0,0,255),2)
            # cv2.line(frame,(286,358),(217,263),(0,0,255),2)
            # cv2.line(frame,(217,263),(199,188),(0,0,255),2)
            # cv2.line(frame,(199,188),(169,154),(0,0,255),2)
           
            if not ret : # check the frames 
                break
            
            if value < len(meta_data)-1:
                meta_data_frame_number = meta_data[value][0] # Extracting meta_data frame Number
                # print(meta_data_frame_number)
            if value < len(meta_data)-1 and meta_data_frame_number ==  frame_count :
                # print("hello")
                coordinates = meta_data[value][1] # Extracting meta_data coordinates
                x1 = int(coordinates[0]) # x1 
                y1 = int(coordinates[1]) # y1
                x2 = int(coordinates[2]) # x2
                y2 = int(coordinates[3]) # y2
                # print(coordinates)
    
                # if (x1>=169 and y2>=154) and (x2<=434 and y2<=366) :
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle 
                
                # call function to check the next meta_data frame number same to current video frame or not 
                value = check_next_frame(frame_count,meta_data,frame,value,out) 
                
            else :
                # coordinates = meta_data[value][1] # Extracting meta_data coordinates
                # x1 = int(coordinates[0]) # x1 
                # y1 = int(coordinates[1]) # y1
                # x2 = int(coordinates[2]) # x2
                # y2 = int(coordinates[3]) # y2
                # # if (x1>=169 and y2>=154) and (x2<=434 and y2<=366) :
                # cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle 
                
                # draw_box_on_left_frame(meta_data,frame,value,out)
                out.write(frame) # write frame on rendered video
    
                
                
        
            
    
        cap.release() # video released
        out.release() # rendered_video released
       
        
        return True
    except Exception as err:
        logger.warning(f"Issue is {err}")
        logger.exception(f"issue")
        return False
    finally:
        logger.info("_Draw Co-ordinates on video Code  End")
        logger.info(f"Execution Time : {time.time() - start_time}")


# define function to check the next meta_data_frame is same to current video frame or not 

def check_next_frame(frame_count,meta_data,frame,value,out):
    while value+1 < len(meta_data)-1 and frame_count == meta_data[value+1][0] :
        coordinates = meta_data[value+1][1] # Extracting next meta_data coordinates
        x1 = int(coordinates[0])
        y1 = int(coordinates[1])
        x2 = int(coordinates[2])
        y2 = int(coordinates[3])
        # if (x1>=169 and y2>=154) and (x2<=434 and y2<=366) :
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle
        value = value + 1 
        
    out.write(frame) # write frame
    
    value = value + 1
    
    return value





def find_meta_data(detectron_json_path):
    with open(detectron_json_path,'r') as file :
        data = json.load(file)
    meta_data = []
    
    length = len(data['object_data'])
    for i in range(length):
        meta_value = []
        frame_number =data['object_data'][i]['frame_no']
        coordinates = data['object_data'][i]['co_ordinates']
        meta_value.append(frame_number)
        meta_value.append(coordinates)
        meta_data.append(meta_value)

    # print(meta_data)
    return meta_data

meta_data =  find_meta_data('/home/ubuntu/Try_code/camera_ip_101/json/compare_area.json')

video_path = '/home/ubuntu/Try_code/camera_ip_101/videos/camera_ip_101_2 - Made with Clipchamp.mp4'
uploaded_video_path = '/home/ubuntu/Try_code/camera_ip_101/rendered_video/compare_area_video_101_6.mp4'
# meta_data =  find_meta_data('/home/ubuntu/Try_code/Area_json/51221.json')

# Mask_RCNN_json_path = '/home/ubuntu/Try_code/error_frame_51221.json'

draw_video_coordinates(video_path,uploaded_video_path,meta_data,file_name='result')