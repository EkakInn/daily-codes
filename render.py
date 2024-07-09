import pandas
import cv2
from loguru import logger # import logger
file_name='/home/ubuntu/testing/object_detection/object1.json'
video_path = '/home/ubuntu/testing/object_detection/scenario3_1 (online-video-cutter.com).mp4'
uploaded_video_path ='/home/ubuntu/testing/object_detection/out.mp4'
result ='result'
# file=pandas.read_json('/home/ubuntu/testing/object_detection/cam3_1.json')
# print(file)

# df=pandas.DataFrame(data=file['object_data'])
# print(df)

list_data=[]

from json import load
with open(file_name,mode='r') as file:
    data = load(file)
    object_data=data['Object']

    for each_json in object_data:
        # print(i['co_ordinates'])
        co_ordinates=each_json['Coordinates']
        frame_no=each_json['Frame_Number']
        list_data.append((frame_no,co_ordinates))
        # print(frame_no,co_ordinates)
# print(list_data)
    
# for each_row in list_data:
#     print(each_row)

# print("4 Index",list_data[4])



def draw_video_coordinates(video_path,uploaded_video_path,meta_data,file_name):
    
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
        
        
        # for i in meta_data: # get the metadata from database
            
        #     meta_data_frame_number =i[0] # Extracting the frame Number from metadata
        #     # print(i)
           
        #     # check json data to current json data continue to do when different its found
        #         #0
        #     while meta_data_frame_number !=Frame_Number: # Comparsion between meta_data_frame_number and Video frame_number
        #         ret , frame =cap.read()
               
        #         if not ret:
        #             break
        #         Frame_Number+=1
        #         if meta_data_frame_number == Frame_Number :
        #             coordinates = i[1]
        #             x1 = int(coordinates[0])
        #             y1 = int(coordinates[1])
        #             x2 = int(coordinates[2])
        #             y2 = int(coordinates[3])
        #             cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        #             out.write(frame)
        #             logger.info(f"frame_{Frame_Number}_write")
               
        #         else :
        #             out.write(frame)
        #             logger.info(f"frame_{Frame_Number}_write")
                    
               
            
        
        value = 0 
        
        
        #  vertices = np.array([[((367,272),(526,224), (898,366),(918,579),(620,675),(620,594),(429,399),(404,305),(367,272))]], dtype=np.int32)
        while True :
            ret , frame = cap.read() # read video frames 
            frame_count +=1 # point to video frames
            
            # draw box on Area of Interest 
            cv2.line(frame,(367,272),(526,224),(0,0,255),2)
            cv2.line(frame,(526,224),(898,366),(0,0,255),2)
            cv2.line(frame,(898,366),(918,579),(0,0,255),2)
            cv2.line(frame,(918,579),(620,675),(0,0,255),2)
            cv2.line(frame,(620,675),(620,594),(0,0,255),2)
            cv2.line(frame,(620,594),(429,399),(0,0,255),2)
            cv2.line(frame,(429,399),(404,305),(0,0,255),2)
            cv2.line(frame,(404,305),(367,272),(0,0,255),2)
           
            if not ret : # check the frames 
                break
            
            if value < len(meta_data):
                meta_data_frame_number = meta_data[value][0] # Extracting meta_data frame Number
                # print(meta_data_frame_number)
            if value < len(meta_data) and meta_data_frame_number ==  frame_count :
                # print("hello")
                coordinates = meta_data[value][1] # Extracting meta_data coordinates
                x1 = int(coordinates[0]) # x1 
                y1 = int(coordinates[1]) # y1
                x2 = int(coordinates[2]) # x2
                y2 = int(coordinates[3]) # y2
                # print(coordinates)
    
                
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle 
                
                # call function to check the next meta_data frame number same to current video frame or not 
                value = check_next_frame(frame_count,meta_data,frame,value,out) 
                
            else :
                out.write(frame) # write frame on rendered video
                # cv2.imwrite(f'/home/ubuntu/ganecos-backend1/cam3_rendered_videos/frames/Frame_{frame_count}.jpg',frame)
                logger.info(f'Process Frame {frame_count}')
                
                
        
            
    
        cap.release() # video released
        out.release() # rendered_video released
       
        
        return True
    except Exception as err:
        logger.warning(f"Issue is {err}")
        logger.exception(f"issue")
        return False
    finally:
        logger.info("_Draw Co-ordinates on video Code  End")


# define function to check the next meta_data_frame is same to current video frame or not 

def check_next_frame(frame_count,meta_data,frame,value,out):
    while value+1 < len(meta_data) and frame_count == meta_data[value+1][0] :
        coordinates = meta_data[value+1][1] # Extracting next meta_data coordinates
        x1 = int(coordinates[0])
        y1 = int(coordinates[1])
        x2 = int(coordinates[2])
        y2 = int(coordinates[3])
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) # draw rectangle
        logger.info(f'Process Frame {frame_count}')
        value = value + 1 
        
    out.write(frame) # write frame
    # cv2.imwrite(f'/home/ubuntu/ganecos-backend1/cam3_rendered_videos/frames/Frame_{frame_count}.jpg',frame)
    logger.info(f'Process Frame {frame_count}')
    value = value + 1
    
    return value


if __name__ =='__main__':
     draw_video_coordinates(video_path,uploaded_video_path,list_data,result)