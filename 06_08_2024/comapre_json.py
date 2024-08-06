import json
from loguru import logger # import logger
import cv2 # import cv2
import time 

def compare_json_value(meta_data,Mask_R_CNN_json_path,List_of_error_frame):
    ''' This function is used for compare the detectron and mask R-CNN value 

            1) If detectron error frame coordinates have same mask R-CNN frame coordinates than no change
            2) If detectron error frame coordinates have not same to mask R-CNN coordinates than coordinates will zero 
             
    for Example  error_frame = 12 and coordinates =[1,2,3,4] have no match to mask R-CNN coordinates than it will be zero [0,0,0,0]
    '''
    

    with open(Mask_R_CNN_json_path,'r') as f:
        mask_data = json.load(f)
    mask_data_length = len(mask_data['object_data'])
    # print(mask_data)

    updated_meta_data=[]
    try :
        for index_value_of_mask_data in range(mask_data_length):

            for index_value_of_meta_data in range(len(meta_data)):

                detectron_frame= meta_data[index_value_of_meta_data][0]
                detectron_coordinates = meta_data[index_value_of_meta_data][1]

                # print(meta_data[index_value_of_meta_data])

                if detectron_frame in List_of_error_frame :

                    if detectron_frame == mask_data['object_data'][index_value_of_mask_data]['frame_no'] and detectron_coordinates != mask_data['object_data'][index_value_of_mask_data]['co_ordinates'] :
                        
                        # meta_data[j] = mask_data['object_data'][i]['frame_no'] ,mask_data['object_data'][i]['co_ordinates']
                        meta_data[index_value_of_meta_data][1]=[0,0,0,0]
                        updated_meta_data.append(meta_data[index_value_of_meta_data])
                        print("updated meta data",meta_data[index_value_of_meta_data])

                    else:
                        meta_data[index_value_of_meta_data][0] = mask_data['object_data'][index_value_of_mask_data]['frame_no'] 
                        meta_data[index_value_of_meta_data][1]= mask_data['object_data'][index_value_of_mask_data]['co_ordinates']
                        # print(meta_data[index_value_of_meta_data])
                        print("updated meta data",meta_data[index_value_of_meta_data])

                else :
                    updated_meta_data.append(meta_data[index_value_of_meta_data])

    except Exception as err:
        logger.exception(f"Issue is {err}")

    print(updated_meta_data)
    return updated_meta_data               








# define function to draw boundary boxes on rendered video
def draw_video_coordinates(video_path,uploaded_video_path,meta_data):
    ''' This function is used to draw the boundary box with help of analysis cooordinates values'''
   
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
        next_frame_count= 0
        index_count = 0

        while True :
            ret , frame = cap.read() # read video frames 
            frame_count +=1 # point to video frames
            
            # draw box on Area of Interest 
            cv2.line(frame,(169,154),(252,130),(0,0,255),2)
            cv2.line(frame,(252,130),(292,152),(0,0,255),2)
            cv2.line(frame,(292,152),(434,218),(0,0,255),2)
            cv2.line(frame,(434,218),(431,366),(0,0,255),2)
            cv2.line(frame,(431,366),(307,431),(0,0,255),2)
            cv2.line(frame,(307,431),(286,358),(0,0,255),2)
            cv2.line(frame,(286,358),(217,263),(0,0,255),2)
            cv2.line(frame,(217,263),(199,188),(0,0,255),2)
            cv2.line(frame,(199,188),(169,154),(0,0,255),2)
           
            if not ret : # check the frames 
                break
            
            if value <=len(meta_data)-1:
                meta_data_frame_number = meta_data[value][0] # Extracting meta_data frame Number
        
                if value <=len(meta_data)-1 and meta_data_frame_number ==  frame_count :
    
                    coordinates = meta_data[value][1] # Extracting meta_data coordinates
                    x1 = int(coordinates[0]) # x1 
                    y1 = int(coordinates[1]) # y1
                    x2 = int(coordinates[2]) # x2
                    y2 = int(coordinates[3]) # y2
        
        
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle 

                    index_count=0

                    # call function to check the next meta_data frame number same to current video frame or not 
                    value,index_count = check_next_frame(frame_count,meta_data,frame,value,out,index_count) 

                    next_frame_count = 0
                    
                else :
                    

                    if index_count==0 and value >=1 :

                        if frame_count > meta_data[value-1][0] and next_frame_count <=10:
                            coordinates = meta_data[value-1][1] # Extracting meta_data coordinates
                            x1 = int(coordinates[0]) # x1 
                            y1 = int(coordinates[1]) # y1
                            x2 = int(coordinates[2]) # x2
                            y2 = int(coordinates[3]) # y2
                    
        
                            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle 

                            value = value -1

                            value = draw_box_on_right_frame(meta_data,frame,value,out)

                            next_frame_count+=1

                        else:
                            out.write(frame)

                    elif index_count > 0 and value >=1 :

                        if frame_count > meta_data[value-index_count][0] and next_frame_count <=10:
                            coordinates = meta_data[value-index_count][1] # Extracting meta_data coordinates
                            x1 = int(coordinates[0]) # x1 
                            y1 = int(coordinates[1]) # y1
                            x2 = int(coordinates[2]) # x2
                            y2 = int(coordinates[3]) # y2
                            # print(coordinates)
        
                            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle

                            value = value-index_count

                            value = draw_box_on_right_frame(meta_data,frame,value,out)

                            next_frame_count+=1

                        else:

                            out.write(frame)
                    else:

                        out.write(frame)

            else:
                if index_count==0 and value >=1 :

                        if frame_count > meta_data[value-1][0] and next_frame_count <=10:
                            coordinates = meta_data[value-1][1] # Extracting meta_data coordinates
                            x1 = int(coordinates[0]) # x1 
                            y1 = int(coordinates[1]) # y1
                            x2 = int(coordinates[2]) # x2
                            y2 = int(coordinates[3]) # y2
                            # print(coordinates)
        
                            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle 

                            value = value -1

                            value = draw_box_on_right_frame(meta_data,frame,value,out)

                            next_frame_count+=1

                        else:
                            out.write(frame)

                elif index_count > 0 and value >=1 :

                    if frame_count > meta_data[value-index_count][0] and next_frame_count <=10:
                        coordinates = meta_data[value-index_count][1] # Extracting meta_data coordinates
                        x1 = int(coordinates[0]) # x1 
                        y1 = int(coordinates[1]) # y1
                        x2 = int(coordinates[2]) # x2
                        y2 = int(coordinates[3]) # y2
                        # print(coordinates)
    
                        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle

                        value = value-index_count

                        value = draw_box_on_right_frame(meta_data,frame,value,out)

                        next_frame_count+=1

                    else:

                        out.write(frame)
                else:

                    out.write(frame)

            
        
                
                
        
            
    
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

def check_next_frame(frame_count,meta_data,frame,value,out,index_count):
    '''
        This function is used to check the next json frame have same value or not 
            1) If next json frame value is same to the current value of frame number than draw the boundary box on current frame 
            2) If next json frame value is not same to the current value frame than it will return the one increased the json value index
    '''

    while value+1 < len(meta_data)-1 and frame_count == meta_data[value+1][0] :
        coordinates = meta_data[value+1][1] # Extracting next meta_data coordinates
        x1 = int(coordinates[0])
        y1 = int(coordinates[1])
        x2 = int(coordinates[2])
        y2 = int(coordinates[3])

        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle
        value = value + 1 
        index_count = index_count + 1
        
    out.write(frame) # write frame
    
    value = value + 1
    index_count= index_count + 1
    
    return value,index_count

# define function to check the having any more coordinates on same frame  

def draw_box_on_right_frame(meta_data,frame,value,out):
    '''This function is used to check the next json frame value is same or not
            1) If next json value is same to the current json value than draw the boundary box 
            2) If next json value is not same to the current json value than return the one increased json value Index
    '''

    while value+1 < len(meta_data)-1 and meta_data[value][0]==meta_data[value+1][0]:
        coordinates = meta_data[value+1][1] # Extracting next meta_data coordinates
        x1 = int(coordinates[0]) # x1
        y1 = int(coordinates[1]) # y1
        x2 = int(coordinates[2]) # x2
        y2 = int(coordinates[3]) # y2

        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) 

        value = value + 1

    out.write(frame)

    value = value + 1

    return value





def find_meta_data(detectron_json_path):
    '''
    This function is uesd for find meta data from detectron json
       in the format of [[12,[1,2,3,4], .......... ]
    '''

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




meta_data =  find_meta_data('/home/ubuntu/Try_code/cam3_videos_json/un_uploaded_json/cam3_58813.json')



video_path = '/home/ubuntu/Try_code/cam3_videos/Cam3__2024_08_02__11_53_58813_video.mp4'
uploaded_video_path = '/home/ubuntu/Try_code/videos/detectron_video__58813__10.mp4'
Mask_RCNN_json_path = '/home/ubuntu/Try_code/cam3_videos_json/error_frame_json/Mask_R_CNN_60673.json'
List_of_error_frames = [1884, 1896, 5664]
# 
# final_meta_data = compare_json_value(meta_data,Mask_RCNN_json_path,List_of_error_frames)
# print(final_meta_data)
draw_video_coordinates(video_path,uploaded_video_path,meta_data)